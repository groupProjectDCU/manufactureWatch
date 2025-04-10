/**
 * Simple Alert Auto-Dismissal
 * 
 * This script automatically dismisses all alert messages after a specified delay.
 * It doesn't rely on Bootstrap's JavaScript API to avoid timing issues.
 */

// Set the timeout duration in milliseconds
const ALERT_TIMEOUT = 4000; // 4 seconds

// Simple function to dismiss all alerts
function dismissAlerts() {
  // Find all alerts
  const alerts = document.querySelectorAll('.alert');
  
  // For each alert, set a timeout to remove it
  alerts.forEach(function(alert) {
    // Don't process alerts that have already been marked
    if (alert.getAttribute('data-timeout-set') === 'true') return;
    
    // Mark this alert to avoid duplicate timers
    alert.setAttribute('data-timeout-set', 'true');
    
    // Set timeout to remove the alert
    setTimeout(function() {
      // Simple fade out effect
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      
      // Remove from DOM after fade completes
      setTimeout(function() {
        if (alert.parentNode) {
          alert.parentNode.removeChild(alert);
        }
      }, 500);
    }, ALERT_TIMEOUT);
  });
}

// Run on page load
window.addEventListener('load', dismissAlerts);

// Run immediately in case page is already loaded
dismissAlerts();

// Set up a periodic check for new alerts (helpful for dynamically added alerts)
setInterval(dismissAlerts, 1000); 