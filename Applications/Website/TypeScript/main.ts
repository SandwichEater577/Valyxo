// Valyxo Website TypeScript
// Main entry point

document.addEventListener("DOMContentLoaded", () => {
  console.log("Valyxo website loaded (TypeScript)");

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener(
      "click",
      function (this: HTMLAnchorElement, e: Event) {
        const href = this.getAttribute("href");
        if (href) {
          const target = document.querySelector(href);
          if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: "smooth" });
          }
        }
      }
    );
  });

  // Add active class to current nav link
  const currentPage = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("nav ul li a").forEach((link) => {
    if (link.getAttribute("href") === currentPage) {
      link.classList.add("active");
    }
  });
});
