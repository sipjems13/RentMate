import { supabase } from './supabase.js';

// Navigation interactivity
document.addEventListener("DOMContentLoaded", () => {
  const navItems = document.querySelectorAll(".nav-item");

  navItems.forEach((item) => {
    item.addEventListener("click", function (e) {
      e.preventDefault();

      // Remove active class from all items
      navItems.forEach((nav) => nav.classList.remove("active"));

      // Add active class to clicked item
      this.classList.add("active");

      // Get the page name
      const page = this.getAttribute("data-page");
      console.log("[v0] Navigating to:", page);

      // Update dashboard title/content
      updateDashboardContent(page);
    });
  });

  // Logout button handler
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
      try {
        // Supabase sign out (if logged in via Supabase)
        await supabase.auth.signOut();
      } catch (error) {
        console.warn("Supabase sign-out skipped or failed:", error);
      }

      // Clear local/session storage
      localStorage.clear();
      sessionStorage.clear();

      // Redirect to homepage
      window.location.href = '/';
    });
  }

  // Profile icon click handler
  const profileIcon = document.querySelector(".profile-icon");
  if (profileIcon) {
    profileIcon.addEventListener("click", () => {
      console.log("[v0] Profile icon clicked");
      alert("Profile menu coming soon!");
    });
  }
});

// Update dashboard title/content
function updateDashboardContent(page) {
  const dashboardTitle = document.querySelector(".dashboard-title");

  // Capitalize first letter
  const pageTitle = page.charAt(0).toUpperCase() + page.slice(1);
  dashboardTitle.textContent = pageTitle;

  console.log("[v0] Dashboard content updated to:", pageTitle);
}
