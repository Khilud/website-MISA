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
        handleServiceSelection.call(serviceSelect);
    }
}

function handleServiceSelection() {
    const selectedId = this.value;
    const detailsDiv = document.getElementById('serviceDetails');
    const infoDiv = document.getElementById('serviceInfo');
    const careerFieldsDiv = document.getElementById('careerFields');
    const tourFieldsDiv = document.getElementById('tourFields');
    const languageFieldsDiv = document.getElementById('languageFields');
    const housingFieldsDiv = document.getElementById('housingFields');
    const otherLanguageField = document.getElementById('otherLanguageField');
    const translationDirectionField = document.getElementById('translationDirectionField');
    
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

        if (careerFieldsDiv) {
            const isCareer = service.category === 'Career' && ['Internship', 'Job Application'].includes(service.subcategory);
            careerFieldsDiv.style.display = isCareer ? 'block' : 'none';
        }

        if (tourFieldsDiv) {
            const isGroupTour = service.category === 'Group Tour' && service.subcategory === 'Sicily Tour';
            tourFieldsDiv.style.display = isGroupTour ? 'block' : 'none';
        }

        if (housingFieldsDiv) {
            const isPermanentHousing = service.category === 'Housing' && service.subcategory === 'Permanent';
            housingFieldsDiv.style.display = isPermanentHousing ? 'block' : 'none';
        }

        if (languageFieldsDiv) {
            const isLanguageOption = service.category === 'Language' && ['Other Language', 'Translation'].includes(service.subcategory);
            languageFieldsDiv.style.display = isLanguageOption ? 'block' : 'none';
        }

        if (otherLanguageField) {
            const isOtherLanguage = service.category === 'Language' && service.subcategory === 'Other Language';
            otherLanguageField.style.display = isOtherLanguage ? 'block' : 'none';
        }

        if (translationDirectionField) {
            const isTranslation = service.category === 'Language' && service.subcategory === 'Translation';
            translationDirectionField.style.display = isTranslation ? 'block' : 'none';
        }
    } else {
        detailsDiv.style.display = 'none';
        if (careerFieldsDiv) {
            careerFieldsDiv.style.display = 'none';
        }
        if (tourFieldsDiv) {
            tourFieldsDiv.style.display = 'none';
        }
        if (housingFieldsDiv) {
            housingFieldsDiv.style.display = 'none';
        }
        if (languageFieldsDiv) {
            languageFieldsDiv.style.display = 'none';
        }
        if (otherLanguageField) {
            otherLanguageField.style.display = 'none';
        }
        if (translationDirectionField) {
            translationDirectionField.style.display = 'none';
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initServiceRequest();
});
