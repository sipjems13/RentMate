# Supabase Setup Guide

## 1. Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up or log in to your account
3. Click "New Project"
4. Choose your organization
5. Enter project details:
   - **Name**: RentMate (or your preferred name)
   - **Database Password**: Choose a strong password
   - **Region**: Choose the closest region to your users
6. Click "Create new project"

## 2. Get Your Project Credentials

1. Once your project is created, go to **Settings** → **API**
2. Copy the following values:
   - **Project URL** (looks like: `https://your-project-id.supabase.co`)
   - **Anon/Public Key** (starts with `eyJ...`)

## 3. Configure Your Application

1. Open `backend/static/supabase.js`
2. Replace the placeholder values:
   ```javascript
   const SUPABASE_URL = 'YOUR_SUPABASE_URL'; // Replace with your Project URL
   const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY'; // Replace with your Anon Key
   ```

## 4. Set Up Authentication

1. In your Supabase dashboard, go to **Authentication** → **Settings**
2. Configure the following:
   - **Site URL**: `http://127.0.0.1:8000` (for development)
   - **Redirect URLs**: Add `http://127.0.0.1:8000/dashboard/`
   - **Email confirmation**: Disable for development (optional)

## 5. Database Schema (Optional)

If you want to store additional user data, you can create a `profiles` table:

```sql
-- Run this in the SQL Editor in your Supabase dashboard
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  role TEXT CHECK (role IN ('landlord', 'tenant')),
  address TEXT,
  phone TEXT,
  city TEXT,
  state TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON profiles
  FOR INSERT WITH CHECK (auth.uid() = id);
```

## 6. Test the Integration

1. Restart your Django server
2. Try registering a new landlord account
3. Try logging in with the new account
4. Check the Supabase dashboard to see the new user

## 7. Production Setup

For production deployment:

1. Update the Site URL and Redirect URLs in Supabase
2. Consider enabling email confirmation
3. Set up proper CORS policies
4. Use environment variables for credentials

## Troubleshooting

- **"Supabase client not available"**: Make sure the Supabase script is loaded before your custom scripts
- **CORS errors**: Check your Supabase project settings for allowed origins
- **Authentication errors**: Verify your credentials and project URL
- **Database errors**: Check your database schema and RLS policies
