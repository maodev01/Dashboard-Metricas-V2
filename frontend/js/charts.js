// Módulo para manejo de gráficos con Chart.js

let weatherChart = null;
let cryptoChart = null;

// Función para crear/actualizar gráfico del clima
function createWeatherChart(data) {
    const ctx = document.getElementById('weatherChart');
    
    if (!data || data.length === 0) {
        ctx.innerHTML = '<p class="text-center text-gray-500 py-8">No hay datos disponibles</p>';
        return;
    }

    // Destruir gráfico anterior si existe
    if (weatherChart) {
        weatherChart.destroy();
    }

    // Preparar datos
    const labels = data.map(d => formatDate(d.date));
    const temperatures = data.map(d => d.temperature);
    const humidity = data.map(d => d.humidity);
    const windSpeed = data.map(d => d.wind_speed);

    // Crear nuevo gráfico
    weatherChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Temperatura (°C)',
                    data: temperatures,
                    borderColor: CONFIG.CHART_COLORS.danger,
                    backgroundColor: CONFIG.CHART_COLORS.dangerLight,
                    yAxisID: 'y',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Humedad (%)',
                    data: humidity,
                    borderColor: CONFIG.CHART_COLORS.info,
                    backgroundColor: CONFIG.CHART_COLORS.infoLight,
                    yAxisID: 'y1',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Viento (m/s)',
                    data: windSpeed,
                    borderColor: CONFIG.CHART_COLORS.success,
                    backgroundColor: CONFIG.CHART_COLORS.successLight,
                    yAxisID: 'y1',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            ...CONFIG.CHART_OPTIONS,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                x: {
                    display: true,
                    grid: {
                        display: false
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Temperatura (°C)'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Humedad (%) / Viento (m/s)'
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                }
            }
        }
    });
}

// Función para crear/actualizar gráfico de criptomonedas
function createCryptoChart(data) {
    const ctx = document.getElementById('cryptoChart');
    
    if (!data || data.length === 0) {
        ctx.innerHTML = '<p class="text-center text-gray-500 py-8">No hay datos disponibles</p>';
        return;
    }

    // Destruir gráfico anterior si existe
    if (cryptoChart) {
        cryptoChart.destroy();
    }

    // Agrupar datos por símbolo
    const groupedData = {};
    data.forEach(d => {
        if (!groupedData[d.symbol]) {
            groupedData[d.symbol] = [];
        }
        groupedData[d.symbol].push(d);
    });

    // Obtener fechas únicas
    const labels = [...new Set(data.map(d => formatDate(d.date)))].sort();

    // Colores para diferentes criptomonedas
    const colors = [
        { border: CONFIG.CHART_COLORS.warning, bg: CONFIG.CHART_COLORS.warningLight },
        { border: CONFIG.CHART_COLORS.info, bg: CONFIG.CHART_COLORS.infoLight },
        { border: CONFIG.CHART_COLORS.success, bg: CONFIG.CHART_COLORS.successLight },
        { border: CONFIG.CHART_COLORS.primary, bg: CONFIG.CHART_COLORS.primaryLight },
    ];

    // Crear datasets
    const datasets = Object.keys(groupedData).map((symbol, index) => {
        const prices = labels.map(label => {
            const item = groupedData[symbol].find(d => formatDate(d.date) === label);
            return item ? item.current_price : null;
        });

        return {
            label: symbol,
            data: prices,
            borderColor: colors[index % colors.length].border,
            backgroundColor: colors[index % colors.length].bg,
            tension: 0.4,
            fill: false
        };
    });

    // Crear gráfico
    cryptoChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            ...CONFIG.CHART_OPTIONS,
            scales: {
                x: {
                    display: true,
                    grid: {
                        display: false
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Precio (USD)'
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + formatNumber(value, 2);
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += formatCurrency(context.parsed.y, 'USD');
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });
}

// Función para crear gráfico de barras para comparación de criptos
function createCryptoComparisonChart(data, containerId) {
    const ctx = document.getElementById(containerId);
    
    if (!data || data.length === 0) return;

    const labels = data.map(d => d.symbol);
    const prices = data.map(d => d.current_price);
    const changes = data.map(d => d.price_change_percentage_24h);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Precio Actual (USD)',
                    data: prices,
                    backgroundColor: CONFIG.CHART_COLORS.primaryLight,
                    borderColor: CONFIG.CHART_COLORS.primary,
                    borderWidth: 2
                }
            ]
        },
        options: {
            ...CONFIG.CHART_OPTIONS,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + formatNumber(value, 2);
                        }
                    }
                }
            }
        }
    });
}