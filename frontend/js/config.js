// Configuración global de la aplicación
const CONFIG = {
    // URL base de la API
    API_BASE_URL: 'http://localhost:8000/api',

    // Colores para los gráficos
    CHART_COLORS: {
        primary: 'rgba(102, 126, 234, 1)',
        primaryLight: 'rgba(102, 126, 234, 0.2)',
        secondary: 'rgba(118, 75, 162, 1)',
        secondaryLight: 'rgba(118, 75, 162, 0.2)',
        success: 'rgba(34, 197, 94, 1)',
        successLight: 'rgba(34, 197, 94, 0.2)',
        warning: 'rgba(251, 191, 36, 1)',
        warningLight: 'rgba(251, 191, 36, 0.2)',
        danger: 'rgba(239, 68, 68, 1)',
        dangerLight: 'rgba(239, 68, 68, 0.2)',
        info: 'rgba(59, 130, 246, 1)',
        infoLight: 'rgba(59, 130, 246, 0.2)',
    },

    // Configuración de criptomonedas a mostrar
    CRYPTO_SYMBOLS: ['BTC', 'ETH', 'ADA', 'SOL'],

    // Número de días por defecto para mostrar en gráficos
    DEFAULT_DAYS_RANGE: 7,

    // Opciones por defecto de Chart.js
    CHART_OPTIONS: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                display: true,
                position: 'top',
            },
            tooltip: {
                mode: 'index',
                intersect: false,
            }
        },
        scales: {
            x: {
                grid: {
                    display: false
                }
            },
            y: {
                beginAtZero: false,
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)'
                }
            }
        }
    }
};

// Función para formatear fechas
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    return date.toISOString().split('T')[0];
}

// Función para formatear fecha y hora
function formatDateTime(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    return date.toLocaleString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Función para formatear números con separadores de miles
function formatNumber(num, decimals = 2) {
    if (num === null || num === undefined) return 'N/A';
    return new Intl.NumberFormat('es-ES', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(num);
}

// Función para formatear moneda
function formatCurrency(num, currency = 'USD') {
    if (num === null || num === undefined) return 'N/A';
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: currency
    }).format(num);
}

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    const colors = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        warning: 'bg-yellow-500',
        info: 'bg-blue-500'
    };

    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 transform transition-all duration-300`;
    notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;

    document.body.appendChild(notification);

    // Animar entrada
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 10);

    // Remover después de 3 segundos
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Inicializar fechas por defecto
function initializeDates() {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - CONFIG.DEFAULT_DAYS_RANGE);

    document.getElementById('startDate').value = formatDate(startDate);
    document.getElementById('endDate').value = formatDate(endDate);
}

// Configuración de auto-refresh
CONFIG.AUTO_REFRESH_ENABLED = true;
CONFIG.AUTO_REFRESH_INTERVAL = 300000; // 2 minutos en milisegundos
