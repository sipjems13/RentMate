function handleLogin(event) {
  event.preventDefault()

  const email = document.getElementById("email").value
  const password = document.getElementById("password").value

  console.log("Login attempt:", { email, password })

  // Add your login logic here
  alert("Login functionality would be implemented here")
}

function handleRegister(event) {
  event.preventDefault()

  const formData = {
    email: document.getElementById("reg-email").value,
    firstName: document.getElementById("first-name").value,
    lastName: document.getElementById("last-name").value,
    address: document.getElementById("address").value,
    phone: document.getElementById("phone").value,
    city: document.getElementById("city").value,
    state: document.getElementById("state").value,
    password: document.getElementById("reg-password").value,
    confirmPassword: document.getElementById("confirm-password").value,
  }

  // Validate passwords match
  if (formData.password !== formData.confirmPassword) {
    alert("Passwords do not match!")
    return
  }

  console.log("Registration attempt:", formData)

  // Add your registration logic here
  alert("Registration functionality would be implemented here")
}
