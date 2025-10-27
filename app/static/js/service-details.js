// Service Details Page JavaScript
// Handles service request/removal functionality

let addServiceUrl = '';
let removeServiceUrl = '';

// Initialize the service details functionality
function initServiceDetails(urls) {
    addServiceUrl = urls.addService;
    removeServiceUrl = urls.removeService;
    
    // Event delegation for service buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('service-btn')) {
            const serviceId = e.target.getAttribute('data-service-id');
            const action = e.target.getAttribute('data-action');
            
            if (action === 'add') {
                addService(serviceId);
            } else if (action === 'remove') {
                removeService(serviceId);
            }
        }
    });
}

function addService(serviceId) {
    fetch(addServiceUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({service_id: parseInt(serviceId)})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message || 'Service request submitted successfully!');
            location.reload();
        } else {
            alert(data.error || 'An error occurred');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your request');
    });
}

function removeService(serviceId) {
    fetch(removeServiceUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({service_id: parseInt(serviceId)})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Service request removed successfully!');
            location.reload();
        } else {
            alert(data.error || 'An error occurred');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your request');
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // URLs will be set by the template
    if (typeof serviceDetailsConfig !== 'undefined') {
        initServiceDetails(serviceDetailsConfig.urls);
    }
});
