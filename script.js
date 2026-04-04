// VoidPay — shared utilities

// Animate number count-up
function animateCount(el, target, prefix = '', suffix = '', duration = 1200) {
  const start = 0;
  const step = (timestamp) => {
    if (!step.startTime) step.startTime = timestamp;
    const progress = Math.min((timestamp - step.startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = prefix + Math.floor(eased * target) + suffix;
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

// Animate progress bars on page load
document.addEventListener('DOMContentLoaded', () => {
  // Stagger animate feature cards
  const cards = document.querySelectorAll('.feature-card, .plan-card');
if (cards.length > 0) {
  cards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(24px)';
    setTimeout(() => {
      card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 100 + i * 80);
  });
}

  // Animate hero stats
  const statValues = document.querySelectorAll('.stat-value');
  statValues.forEach(el => {
    el.style.opacity = '0';
    setTimeout(() => {
      el.style.transition = 'opacity 0.6s';
      el.style.opacity = '1';
    }, 600);
  });
});
