// Service Request Page JavaScript
// Handles dynamic service selection and details display

let serviceDetails = {};

// Initialize the service request functionality
function initServiceRequest() {
    // Read service data from HTML data attribute
    const serviceDataElement = document.getElementById('service-data');
    if (serviceDataElement) {
        try {
            const servicesArray = JSON.parse(serviceDataElement.getAttribute('data-services'));
            // Convert array to object indexed by ID
            serviceDetails = {};
            servicesArray.forEach(service => {
                serviceDetails[service.id] = service;
            });
        } catch (error) {
            console.error('Error parsing service data:', error);
            return;
        }
    }
    
    const serviceSelect = document.getElementById('serviceSelect');
    if (serviceSelect) {
        serviceSelect.addEventListener('change', handleServiceSelection);
    }
}

function handleServiceSelection() {
    const selectedId = this.value;
    const detailsDiv = document.getElementById('serviceDetails');
    const infoDiv = document.getElementById('serviceInfo');
    
    if (selectedId && serviceDetails[selectedId]) {
        const service = serviceDetails[selectedId];
        infoDiv.innerHTML = `
            <h6>${service.name}</h6>
            <p>${service.description}</p>
            <p><strong>Category:</strong> ${service.category}</p>
            ${service.subcategory ? `<p><strong>Type:</strong> ${service.subcategory}</p>` : ''}
            <p><strong>Price: ---</strong></p>
        `;
        detailsDiv.style.display = 'block';
    } else {
        detailsDiv.style.display = 'none';
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initServiceRequest();
});
