from datetime import datetime, timedelta
from typing import Optional
import os
import logging

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from passlib.context import CryptContext
from jose import jwt


# Simple settings (for demo). In production, move to env vars.
JWT_SECRET = "CHANGE_ME_DEV_SECRET"
JWT_ALG = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# Use Supabase Postgres if provided; otherwise fallback to local sqlite for dev
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rentmate.db")


# Create engine with correct connect_args based on dialect
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        isolation_level="AUTOCOMMIT",
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="tenant")  # 'landlord' or 'tenant'
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    landlord = relationship("Landlord", back_populates="user", uselist=False)
    tenant = relationship("Tenant", back_populates="user", uselist=False)


class Landlord(Base):
    __tablename__ = "landlords"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="landlord")


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tenant")


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    landlord_id = Column(Integer, ForeignKey("landlords.id"), nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: Optional[str] = Field(default="tenant")
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALG)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="RentMate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    # Log which DB we are connecting to (mask credentials)
    try:
        logging.basicConfig(level=logging.INFO)
        masked = DATABASE_URL
        if "@" in masked:
            # mask user:pass portion if present
            try:
                prefix, rest = masked.split("@", 1)
                if "//" in prefix:
                    scheme, auth = prefix.split("//", 1)
                    auth_masked = "***:***"
                    masked = f"{scheme}//{auth_masked}@{rest}"
            except Exception:
                pass
        logging.info(f"Connecting to database: {masked}")
    except Exception:
        pass

    Base.metadata.create_all(bind=engine)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "app": "rentmate"}


@app.post("/api/register", response_model=AuthResponse)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(default=None, convert_underscores=False),
):
    existing = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    role = (payload.role or "tenant").lower()
    if role not in {"tenant", "landlord"}:
        raise HTTPException(status_code=400, detail="Invalid role")

    # Enforce: only landlords can create tenants
    # - Creating a landlord account is allowed without auth (bootstrap first landlord)
    # - Creating a tenant requires a valid landlord token
    creator_user: Optional[User] = None
    if role == "tenant":
        if not authorization or not authorization.lower().startswith("bearer "):
            raise HTTPException(status_code=401, detail="Landlord authorization required to create tenant")
        token = authorization.split(" ", 1)[1]
        try:
            payload_jwt = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
            creator_user_id = int(payload_jwt.get("sub"))
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
        creator_user = db.query(User).filter(User.id == creator_user_id).first()
        if not creator_user or creator_user.role != "landlord":
            raise HTTPException(status_code=403, detail="Only landlords can register tenants")

    user = User(
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        role=role,
        first_name=payload.firstName,
        last_name=payload.lastName,
        address=payload.address,
        phone=payload.phone,
        city=payload.city,
        state=payload.state,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create role-specific row
    if role == "landlord":
        db.add(Landlord(user_id=user.id))
    else:
        db.add(Tenant(user_id=user.id))
    db.commit()

    # Do not auto-login newly registered accounts. Return a one-time token for the creator/registrant context.
    # If a landlord created a tenant, keep the landlord logged in by issuing a token for the landlord.
    subject_user_id = creator_user.id if (creator_user and role == "tenant") else user.id
    token = create_access_token(subject=str(subject_user_id))
    return AuthResponse(access_token=token)


@app.post("/api/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(subject=str(user.id))
    return AuthResponse(access_token=token)


