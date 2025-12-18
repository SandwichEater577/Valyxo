// Valyxo Website - Animations & Effects

// Scroll reveal animation
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
};

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("revealed");
      revealObserver.unobserve(entry.target);
    }
  });
}, observerOptions);

// Apply to elements with .reveal class
document.querySelectorAll(".reveal").forEach((el) => {
  revealObserver.observe(el);
});

// Smooth parallax effect on hero section
const hero = document.querySelector(".hero");
if (hero) {
  window.addEventListener("scroll", () => {
    const scroll = window.scrollY;
    if (scroll < window.innerHeight) {
      hero.style.transform = `translateY(${scroll * 0.3}px)`;
      hero.style.opacity = 1 - scroll * 0.002;
    }
  });
}

// Mouse follower glow effect
const createMouseGlow = () => {
  const glow = document.createElement("div");
  glow.className = "mouse-glow";
  document.body.appendChild(glow);

  let mouseX = 0,
    mouseY = 0;
  let glowX = 0,
    glowY = 0;

  document.addEventListener("mousemove", (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  function animate() {
    glowX += (mouseX - glowX) * 0.1;
    glowY += (mouseY - glowY) * 0.1;
    glow.style.left = glowX + "px";
    glow.style.top = glowY + "px";
    requestAnimationFrame(animate);
  }
  animate();
};

// Only enable mouse glow on desktop
if (window.matchMedia("(min-width: 768px)").matches) {
  createMouseGlow();
}

// Feature card mouse tracking
document.querySelectorAll(".feature-card").forEach((card) => {
  card.addEventListener("mousemove", (e) => {
    const rect = card.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    card.style.setProperty("--mouse-x", x + "%");
    card.style.setProperty("--mouse-y", y + "%");
  });
});

// Smooth number counter for stats
function animateCounter(element, target, duration = 2000) {
  let start = 0;
  const increment = target / (duration / 16);

  function update() {
    start += increment;
    if (start < target) {
      element.textContent = Math.floor(start);
      requestAnimationFrame(update);
    } else {
      element.textContent = target;
    }
  }
  update();
}

// Tilt effect for cards
document.querySelectorAll("[data-tilt]").forEach((card) => {
  card.addEventListener("mousemove", (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = (y - centerY) / 20;
    const rotateY = (centerX - x) / 20;

    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
  });

  card.addEventListener("mouseleave", () => {
    card.style.transform =
      "perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)";
  });
});

// Typing animation for terminal
const terminalLines = [
  { text: "$ valyxo init my-project", type: "command" },
  { text: "✓ Project created successfully", type: "success" },
  { text: "$ valyxo run", type: "command" },
  { text: "→ Starting development server...", type: "info" },
  { text: "✓ Ready at http://localhost:3000", type: "success" },
];

// Create cursor element
let cursor = null;
function createCursor() {
  cursor = document.createElement("span");
  cursor.className = "terminal-cursor";
  cursor.textContent = "▌";
  return cursor;
}

async function typeWriter(element, text, speed = 50, codeElement) {
  return new Promise((resolve) => {
    let i = 0;
    function type() {
      if (i < text.length) {
        element.textContent += text.charAt(i);
        // Move cursor to end
        if (cursor && codeElement) {
          codeElement.appendChild(cursor);
        }
        i++;
        setTimeout(type, speed);
      } else {
        resolve();
      }
    }
    type();
  });
}

async function animateTerminal() {
  const codeElement = document.querySelector(".window-content code");
  if (!codeElement) return;

  codeElement.innerHTML = "";
  createCursor();
  codeElement.appendChild(cursor);

  for (const line of terminalLines) {
    const span = document.createElement("span");
    if (line.type === "command") {
      const prompt = document.createElement("span");
      prompt.className = "prompt";
      prompt.textContent = line.text.split(" ")[0] + " ";
      span.appendChild(prompt);
      codeElement.appendChild(span);
      codeElement.appendChild(cursor);
      await typeWriter(
        span,
        line.text.substring(line.text.indexOf(" ") + 1),
        40,
        codeElement
      );
    } else {
      span.className = line.type;
      span.textContent = line.text.charAt(0) + " ";
      const textSpan = document.createElement("span");
      span.appendChild(textSpan);
      codeElement.appendChild(span);
      codeElement.appendChild(cursor);
      await typeWriter(textSpan, line.text.substring(2), 30, codeElement);
      codeElement.appendChild(document.createTextNode("\n"));
      continue;
    }
    codeElement.appendChild(document.createTextNode("\n"));
    await new Promise((r) => setTimeout(r, 300));
  }

  // Keep cursor blinking at the end
  codeElement.appendChild(cursor);
}

// Run terminal animation when in view
const codeWindow = document.querySelector(".code-window");
if (codeWindow) {
  const terminalObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateTerminal();
          terminalObserver.disconnect();
        }
      });
    },
    { threshold: 0.5 }
  );
  terminalObserver.observe(codeWindow);
}

console.log("🚀 Valyxo animations loaded");
