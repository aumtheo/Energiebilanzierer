/**
 * Fetches calculation results from the API based on form data
 * @param {Object} data - Form data as key-value pairs
 * @returns {Promise} - Promise that resolves with the calculation results
 */
async function fetchCalculation(data) {
  try {
    // Convert data object to URL parameters
    const params = new URLSearchParams();
    
    // Add each form field to the params
    for (const [key, value] of Object.entries(data)) {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value);
      }
    }
    
    // Make the API request
    const response = await fetch(`/api/berechnung/?${params.toString()}`);
    
    // Check if the request was successful
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    // Parse the JSON response
    const result = await response.json();
    
    // Update the UI with the calculation results
    updateResultsUI(result);
    
    return result;
  } catch (error) {
    console.error('Error fetching calculation:', error);
    // Optionally show an error message to the user
    // displayErrorMessage('Failed to calculate results. Please try again.');
  }
}

/**
 * Updates the UI with calculation results
 * @param {Object} data - The calculation results from the API
 */
function updateResultsUI(data) {
  // Update building data
  updateElementIfExists('gebaeude_hoehe', data.gebaeudedaten?.hoehe);
  updateElementIfExists('gebaeude_volumen', data.gebaeudedaten?.volumen);
  updateElementIfExists('gebaeude_bgf', data.gebaeudedaten?.bgf);
  updateElementIfExists('gebaeude_nf', data.gebaeudedaten?.nf);
  
  // Update energy usage data
  updateElementIfExists('ne_absolut', data.nutzenergie?.ne_absolut);
  updateElementIfExists('ne_spezifisch', data.nutzenergie?.ne_spezifisch);
  
  // Update electricity demand
  updateElementIfExists('sb_absolut', data.strombedarf?.sb_absolut);
  updateElementIfExists('sb_spezifisch', data.strombedarf?.sb_spezifisch);
  
  // Update heat demand
  updateElementIfExists('wb_absolut', data.waermebedarf?.wb_absolut);
  
  // Update end energy demand
  updateElementIfExists('ee_absolut', data.endenergie?.ee_absolut);
  updateElementIfExists('ee_spezifisch', data.endenergie?.ee_spezifisch);
}

/**
 * Updates an element's text content if the element exists
 * @param {string} elementId - The ID of the element to update
 * @param {*} value - The value to set
 */
function updateElementIfExists(elementId, value) {
  const element = document.getElementById(elementId);
  if (element && value !== undefined && value !== null) {
    // Format numbers to 2 decimal places
    if (typeof value === 'number') {
      element.textContent = value.toFixed(2);
    } else {
      element.textContent = value;
    }
  }
}

/**
 * Initializes form event listeners for live calculation
 */
function initFormListeners() {
  const form = document.querySelector('form');
  if (!form) return;
  
  // Listen for input changes on all form fields
  form.addEventListener('input', function(event) {
    // Get all form data
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    // Fetch calculation with the updated data
    fetchCalculation(data);
  });
  
  // Also update on form submission (without actually submitting)
  form.addEventListener('submit', function(event) {
    // Only prevent default if the data-no-prevent attribute is not present
    if (!form.hasAttribute('data-no-prevent')) {
      event.preventDefault();
    }
    
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    fetchCalculation(data);
  });
}

// Initialize when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
  initFormListeners();
  
  // If there's initial data in the form, fetch calculation on page load
  const form = document.querySelector('form');
  if (form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    // Only fetch if there's at least one non-empty value
    const hasData = Object.values(data).some(value => value !== null && value !== undefined && value !== '');
    if (hasData) {
      fetchCalculation(data);
    }
  }
});