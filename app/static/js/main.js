/* ==========================================================================
   BlogNest – Frontend Interactions & Utilities
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Menu Toggle
  const mobileToggle = document.getElementById('mobileMenuToggle');
  const mobileMenu = document.getElementById('mobileMenu');

  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', () => {
      const isHidden = mobileMenu.style.display === 'none' || !mobileMenu.style.display;
      mobileMenu.style.display = isHidden ? 'flex' : 'none';
    });
  }

  // 2. Alert Dismissal
  const alertCloseBtns = document.querySelectorAll('.alert-close');
  alertCloseBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const alert = e.target.closest('.alert');
      if (alert) {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        setTimeout(() => alert.remove(), 250);
      }
    });
  });

  // Auto-dismiss alerts after 5 seconds
  const autoAlerts = document.querySelectorAll('.alert:not(.alert-danger)');
  autoAlerts.forEach(alert => {
    setTimeout(() => {
      if (alert && alert.parentElement) {
        alert.style.transition = 'all 0.3s ease';
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        setTimeout(() => alert.remove(), 300);
      }
    }, 5000);
  });

  // 3. Live Reading Time & Word Count Calculator in Post Editor
  const contentInput = document.getElementById('postContentInput');
  const wordCountDisplay = document.getElementById('editorWordCount');
  const readingTimeDisplay = document.getElementById('editorReadingTime');

  if (contentInput && (wordCountDisplay || readingTimeDisplay)) {
    const updateStats = () => {
      const text = contentInput.value.trim();
      const words = text ? text.match(/\b\S+\b/g) || [] : [];
      const count = words.length;
      const readingMinutes = Math.max(1, Math.round(count / 200));

      if (wordCountDisplay) {
        wordCountDisplay.textContent = `${count} word${count === 1 ? '' : 's'}`;
      }
      if (readingTimeDisplay) {
        readingTimeDisplay.textContent = `${readingMinutes} min read`;
      }
    };

    contentInput.addEventListener('input', updateStats);
    updateStats(); // Initial trigger
  }

  // 4. Share Link Copy to Clipboard
  const shareBtn = document.getElementById('sharePostBtn');
  if (shareBtn) {
    shareBtn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(window.location.href);
        const originalText = shareBtn.innerHTML;
        shareBtn.innerHTML = '<span>Copied! ✓</span>';
        setTimeout(() => {
          shareBtn.innerHTML = originalText;
        }, 2000);
      } catch (err) {
        console.error('Failed to copy link:', err);
      }
    });
  }
});
