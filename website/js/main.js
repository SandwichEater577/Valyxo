document.addEventListener('DOMContentLoaded', function() {
  initializeNavigation();
  initializeCards();
  initializeButtons();
  initializeFormValidation();
  initializeTabs();
  initializeAnimations();
});

function initializeNavigation() {
  const navLinks = document.querySelectorAll('.nav-menu a');
  const currentLocation = location.pathname;
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (currentLocation.includes(href) && href !== 'index.html') {
      link.classList.add('active');
    } else if (currentLocation === '/' && href === 'index.html') {
      link.classList.add('active');
    }
  });

  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      if (!this.href.includes('#')) {
        navLinks.forEach(l => l.classList.remove('active'));
        this.classList.add('active');
      }
    });
  });
}

function initializeCards() {
  const cards = document.querySelectorAll('.feature-card, .component-card, .project-card, .stat-card');
  
  cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transition = 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
    });

    card.addEventListener('click', function(e) {
      if (this.tagName !== 'A') {
        this.style.transform = 'scale(0.97)';
        setTimeout(() => {
          this.style.transform = '';
        }, 150);
      }
    });
  });
}

function initializeButtons() {
  const buttons = document.querySelectorAll('.btn');
  
  buttons.forEach(btn => {
    btn.addEventListener('mousedown', function() {
      this.style.transform = 'scale(0.98)';
    });

    btn.addEventListener('mouseup', function() {
      this.style.transform = '';
    });

    btn.addEventListener('mouseleave', function() {
      this.style.transform = '';
    });
  });
}

function initializeFormValidation() {
  const forms = document.querySelectorAll('form');
  
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      const inputs = this.querySelectorAll('input[required], textarea[required]');
      let isValid = true;

      inputs.forEach(input => {
        if (!input.value.trim()) {
          input.style.borderColor = 'var(--error)';
          input.style.backgroundColor = 'rgba(255, 107, 107, 0.05)';
          isValid = false;
        } else {
          input.style.borderColor = 'var(--border)';
          input.style.backgroundColor = 'var(--darker)';
        }
      });

      if (!isValid) {
        e.preventDefault();
        showNotification('Please fill in all required fields', 'error');
      }
    });
  });
}

function initializeTabs() {
  const tabButtons = document.querySelectorAll('.tab');
  
  tabButtons.forEach(button => {
    button.addEventListener('click', function() {
      const tabName = this.getAttribute('data-tab');
      
      const tabs = this.parentElement.querySelectorAll('.tab');
      tabs.forEach(tab => tab.classList.remove('active'));
      this.classList.add('active');

      const contents = document.querySelectorAll('.tab-content');
      contents.forEach(content => content.classList.remove('active'));
      
      const activeContent = document.querySelector(`[data-content="${tabName}"]`);
      if (activeContent) {
        activeContent.classList.add('active');
      }
    });
  });
}

function initializeAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animation = 'fadeIn 0.6s ease forwards';
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.feature-card, .component-card, .project-card, .stat-card').forEach(el => {
    observer.observe(el);
  });
}

function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification ${type}`;
  notification.innerHTML = `
    <span>${getIcon(type)}</span>
    <span>${message}</span>
  `;
  
  notification.style.position = 'fixed';
  notification.style.top = '20px';
  notification.style.right = '20px';
  notification.style.zIndex = '9999';
  notification.style.maxWidth = '300px';
  notification.style.animation = 'slideUp 0.3s ease';
  
  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.animation = 'slideUp 0.3s ease reverse';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

function getIcon(type) {
  const icons = {
    success: '✓',
    error: '✕',
    warning: '⚠',
    info: 'ℹ'
  };
  return icons[type] || '•';
}

function smoothScroll(target) {
  const element = document.querySelector(target);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
}

window.showNotification = showNotification;
window.smoothScroll = smoothScroll;
