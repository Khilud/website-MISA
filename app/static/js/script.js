// Script for Service Portal

document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Fade out alerts after 5 seconds
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.classList.add('fade');
            setTimeout(function() {
                alert.style.display = 'none';
            }, 500);
        });
    }, 5000);
});