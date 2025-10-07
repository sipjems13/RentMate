import { supabase } from './supabase.js';

// Navigation interactivity
document.addEventListener("DOMContentLoaded", () => {
    const navItems = document.querySelectorAll(".nav-item")
  
    navItems.forEach((item) => {
      item.addEventListener("click", function (e) {
        e.preventDefault()
  
        // Remove active class from all items
        navItems.forEach((nav) => nav.classList.remove("active"))
  
        // Add active class to clicked item
        this.classList.add("active")
  
        // Get the page name
        const page = this.getAttribute("data-page")
        console.log("[v0] Navigating to:", page)
  
        // Here you can add logic to load different content
        // For now, we'll just update the title
        updateDashboardContent(page)
      })
    })
  })

  const logoutBtn = document.getElementById('logoutBtn')
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
      try {
        // Supabase sign out (if logged in via Supabase)
        await supabase.auth.signOut()
      } catch (_) {}
      // Clear any backend token
      localStorage.removeItem('rentmate_token')
      // Go to landing
      window.location.href = 'index.html'
    })
  }
  
  function updateDashboardContent(page) {
    const dashboardTitle = document.querySelector(".dashboard-title")
  
    // Capitalize first letter
    const pageTitle = page.charAt(0).toUpperCase() + page.slice(1)
    dashboardTitle.textContent = pageTitle
  
    console.log("[v0] Dashboard content updated to:", pageTitle)
  }
  
  // Profile icon click handler
  document.addEventListener("DOMContentLoaded", () => {
    const profileIcon = document.querySelector(".profile-icon")
  
    if (profileIcon) {
      profileIcon.addEventListener("click", () => {
        console.log("[v0] Profile icon clicked")
        // Add profile menu logic here
        alert("Profile menu coming soon!")
      })
    }
  })
  