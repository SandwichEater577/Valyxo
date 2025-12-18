// Valyxo Website JavaScript
// Main entry point

document.addEventListener("DOMContentLoaded", () => {
  console.log("Valyxo website loaded");

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  // Add active class to current nav link
  const currentPage = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("nav ul li a").forEach((link) => {
    if (link.getAttribute("href") === currentPage) {
      link.classList.add("active");
    }
  });
});
