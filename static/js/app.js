// NauticBooking JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Form validation enhancements
    const forms = document.querySelectorAll('form[novalidate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Date validation for reservation forms
    const checkinInput = document.querySelector('input[name="fecha_checkin"]');
    const checkoutInput = document.querySelector('input[name="fecha_checkout"]');
    
    if (checkinInput && checkoutInput) {
        checkinInput.addEventListener('change', validateDates);
        checkoutInput.addEventListener('change', validateDates);
        
        function validateDates() {
            const checkinDate = new Date(checkinInput.value);
            const checkoutDate = new Date(checkoutInput.value);
            
            if (checkinDate && checkoutDate && checkoutDate <= checkinDate) {
                checkoutInput.setCustomValidity('La fecha de check-out debe ser posterior a la fecha de check-in');
            } else {
                checkoutInput.setCustomValidity('');
            }
        }
    }
    
    // Price calculation helpers
    const priceInputs = document.querySelectorAll('input[type="number"][step="0.01"]');
    priceInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Format as currency on blur
            this.addEventListener('blur', function() {
                if (this.value) {
                    this.value = parseFloat(this.value).toFixed(2);
                }
            });
        });
    });
    
    // Promotional code validation
    const promoCodeInput = document.querySelector('input[name="codigo_promocional"]');
    if (promoCodeInput) {
        promoCodeInput.addEventListener('input', function() {
            // Convert to uppercase
            this.value = this.value.toUpperCase();
        });
    }
    
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('button[type="submit"][title="Eliminar"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const confirmed = confirm('¿Está seguro de que desea eliminar esta reserva? Esta acción no se puede deshacer.');
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
    
    // Search form enhancements
    const searchForm = document.querySelector('form[method="GET"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="search_term"]');
        if (searchInput) {
            searchInput.addEventListener('keypress', function(event) {
                if (event.key === 'Enter') {
                    searchForm.submit();
                }
            });
        }
    }
    
    // Tooltip initialization
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Loading states for forms
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                this.disabled = true;
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Procesando...';
                
                // Re-enable button after 5 seconds as fallback
                setTimeout(() => {
                    this.disabled = false;
                    this.textContent = this.getAttribute('data-original-text') || 'Enviar';
                }, 5000);
            }
        });
    });
    
    // Store original button text
    submitButtons.forEach(button => {
        button.setAttribute('data-original-text', button.textContent || button.innerText);
    });
    
    // File input validation
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const maxSize = 10 * 1024 * 1024; // 10MB
                if (file.size > maxSize) {
                    alert('El archivo es demasiado grande. El tamaño máximo es 10MB.');
                    this.value = '';
                    return;
                }
                
                const allowedTypes = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                                    'application/vnd.ms-excel'];
                if (!allowedTypes.includes(file.type)) {
                    alert('Solo se permiten archivos Excel (.xlsx, .xls).');
                    this.value = '';
                    return;
                }
            }
        });
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Print functionality
    const printButtons = document.querySelectorAll('[data-action="print"]');
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            window.print();
        });
    });
    
    // Auto-save form drafts (optional enhancement)
    const autoSaveForms = document.querySelectorAll('form[data-autosave="true"]');
    autoSaveForms.forEach(form => {
        const formData = new FormData(form);
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                // Save form data to localStorage
                const formKey = 'form_draft_' + form.id;
                const currentData = {};
                
                inputs.forEach(inp => {
                    if (inp.type !== 'password') {
                        currentData[inp.name] = inp.value;
                    }
                });
                
                localStorage.setItem(formKey, JSON.stringify(currentData));
            });
        });
        
        // Load saved data on page load
        const formKey = 'form_draft_' + form.id;
        const savedData = localStorage.getItem(formKey);
        if (savedData) {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(key => {
                const input = form.querySelector(`[name="${key}"]`);
                if (input && input.type !== 'password') {
                    input.value = data[key];
                }
            });
        }
        
        // Clear saved data on successful submit
        form.addEventListener('submit', function() {
            localStorage.removeItem(formKey);
        });
    });
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('es-ES').format(new Date(date));
}

function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}
