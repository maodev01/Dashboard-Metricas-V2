// Módulo para manejo de gráficos con Chart.js

let weatherChart = null;
let cryptoChart = null;

// Función para crear/actualizar gráfico del clima
function createWeatherChart(data) {
    const ctx = document.getElementById('weatherChart');

    if (!ctx) {
        console.error('Canvas weatherChart no encontrado');
        return;
    }

    if (!data || data.length === 0) {
        ctx.parentElement.innerHTML = '<p class="text-center text-gray-500 py-8">No hay datos históricos disponibles. Espera unos minutos para que se acumulen datos.</p>';
        return;
    }

    console.log('Creando gráfico de clima con', data.length, 'puntos');

    // Destruir gráfico anterior si existe
    if (weatherChart) {
        weatherChart.destroy();
    }

    // Preparar datos
    const labels = data.map(d => {
        const date = new Date(d.date);
        return date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    });
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
                    borderColor: 'rgb(239, 68, 68)',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    yAxisID: 'y',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2,
                    pointRadius: 3,
                    pointHoverRadius: 5
                },
                {
                    label: 'Humedad (%)',
                    data: humidity,
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    yAxisID: 'y1',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2,
                    pointRadius: 3,
                    pointHoverRadius: 5
                },
                {
                    label: 'Viento (m/s)',
                    data: windSpeed,
                    borderColor: 'rgb(34, 197, 94)',
                    backgroundColor: 'rgba(34, 197, 94, 0.1)',
                    yAxisID: 'y1',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2,
                    pointRadius: 3,
                    pointHoverRadius: 5
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12
                },
                title: {
                    display: true,
                    text: 'Evolución de Condiciones Climáticas',
                    font: {
                        size: 16,
                        weight: 'bold'
                    },
                    padding: {
                        bottom: 20
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Temperatura (°C)',
                        font: {
                            weight: 'bold'
                        }
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
                        text: 'Humedad (%) / Viento (m/s)',
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                }
            }
        }
    });

    console.log('✅ Gráfico de clima creado exitosamente');
}

// Función para crear/actualizar gráfico de criptomonedas
function createCryptoChart(data) {
    const ctx = document.getElementById('cryptoChart');

    if (!ctx) {
        console.error('Canvas cryptoChart no encontrado');
        return;
    }

    if (!data || data.length === 0) {
        ctx.parentElement.innerHTML = '<p class="text-center text-gray-500 py-8">No hay datos históricos disponibles. Espera unos minutos para que se acumulen datos.</p>';
        return;
    }

    console.log('Creando gráfico de crypto con', data.length, 'puntos');

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

    console.log('Símbolos encontrados:', Object.keys(groupedData));

    // Limitar a top 6 criptos por market cap rank
    const topSymbols = Object.keys(groupedData)
        .map(symbol => ({
            symbol,
            rank: Math.min(...groupedData[symbol].map(d => d.market_cap_rank || 999))
        }))
        .sort((a, b) => a.rank - b.rank)
        .slice(0, 6)
        .map(item => item.symbol);

    console.log('Top 6 símbolos para gráfico:', topSymbols);

    // Obtener fechas únicas y ordenarlas
    const allDates = data.map(d => new Date(d.date));
    const uniqueDates = [...new Set(allDates.map(d => d.getTime()))]
        .sort()
        .map(timestamp => new Date(timestamp));

    const labels = uniqueDates.map(date =>
        date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
    );

    // Colores específicos por cripto
    const cryptoColors = {
        'BTC': { border: 'rgb(242, 169, 0)', bg: 'rgba(242, 169, 0, 0.1)' },
        'ETH': { border: 'rgb(98, 126, 234)', bg: 'rgba(98, 126, 234, 0.1)' },
        'BNB': { border: 'rgb(243, 186, 47)', bg: 'rgba(243, 186, 47, 0.1)' },
        'XRP': { border: 'rgb(35, 189, 238)', bg: 'rgba(35, 189, 238, 0.1)' },
        'ADA': { border: 'rgb(0, 51, 173)', bg: 'rgba(0, 51, 173, 0.1)' },
        'SOL': { border: 'rgb(220, 31, 255)', bg: 'rgba(220, 31, 255, 0.1)' }
    };

    // Crear datasets solo para top cryptos
    const datasets = topSymbols.map((symbol) => {
        const cryptoData = groupedData[symbol]
            .sort((a, b) => new Date(a.date) - new Date(b.date));

        const prices = uniqueDates.map(targetDate => {
            const item = cryptoData.find(d => {
                const dataDate = new Date(d.date);
                return Math.abs(dataDate - targetDate) < 60000; // 1 minuto de tolerancia
            });
            return item ? item.current_price : null;
        });

        const color = cryptoColors[symbol] || {
            border: `hsl(${Math.random() * 360}, 70%, 50%)`,
            bg: `hsla(${Math.random() * 360}, 70%, 50%, 0.1)`
        };

        return {
            label: symbol,
            data: prices,
            borderColor: color.border,
            backgroundColor: color.bg,
            borderWidth: 2,
            tension: 0.4,
            fill: false,
            pointRadius: 3,
            pointHoverRadius: 5,
            pointBackgroundColor: color.border,
            pointBorderColor: '#fff',
            pointBorderWidth: 2
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
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US', {
                                    style: 'currency',
                                    currency: 'USD'
                                }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Evolución de Precios de Criptomonedas',
                    font: {
                        size: 16,
                        weight: 'bold'
                    },
                    padding: {
                        bottom: 20
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45,
                        font: {
                            size: 10
                        }
                    }
                },
                y: {
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Precio (USD)',
                        font: {
                            size: 13,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString('en-US');
                        },
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            }
        }
    });

    console.log('✅ Gráfico de crypto creado exitosamente');
}
