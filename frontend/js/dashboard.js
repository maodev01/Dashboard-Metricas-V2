// Módulo principal del dashboard

// ==================== STATS SECTION ====================
async function loadStats() {
    try {
        const stats = await API.getStatsSummary();

        const statsSection = document.getElementById('statsSection');
        statsSection.innerHTML = `
            <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow-lg p-6 text-white card-hover transition duration-300">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-blue-100 text-sm font-medium">Datos del Clima</p>
                        <p class="text-3xl font-bold mt-2">${stats.total_records.weather}</p>
                        <p class="text-blue-100 text-xs mt-2">
                            ${stats.latest_dates.weather ? 'Último: ' + formatDateTime(stats.latest_dates.weather) : 'Sin datos'}
                        </p>
                    </div>
                    <div class="bg-blue-400 bg-opacity-30 rounded-full p-4">
                        <i class="fas fa-cloud-sun text-4xl"></i>
                    </div>
                </div>
            </div>

            <div class="bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-lg shadow-lg p-6 text-white card-hover transition duration-300">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-yellow-100 text-sm font-medium">Criptomonedas</p>
                        <p class="text-3xl font-bold mt-2">${stats.total_records.crypto}</p>
                        <p class="text-yellow-100 text-xs mt-2">
                            ${stats.latest_dates.crypto ? 'Último: ' + formatDateTime(stats.latest_dates.crypto) : 'Sin datos'}
                        </p>
                    </div>
                    <div class="bg-yellow-400 bg-opacity-30 rounded-full p-4">
                        <i class="fab fa-bitcoin text-4xl"></i>
                    </div>
                </div>
            </div>

            <div class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow-lg p-6 text-white card-hover transition duration-300">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-purple-100 text-sm font-medium">TfL Transport</p>
                        <p class="text-3xl font-bold mt-2">${stats.total_records.tfl}</p>
                        <p class="text-purple-100 text-xs mt-2">
                            ${stats.latest_dates.tfl ? 'Último: ' + formatDateTime(stats.latest_dates.tfl) : 'Sin datos'}
                        </p>
                    </div>
                    <div class="bg-purple-400 bg-opacity-30 rounded-full p-4">
                        <i class="fas fa-subway text-4xl"></i>
                    </div>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// ==================== WEATHER SECTION ====================
async function loadWeatherData(startDate, endDate) {
    const loading = document.getElementById('weatherLoading');
    loading.classList.remove('hidden');

    try {
        // Obtener datos actuales
        const currentWeather = await API.getLatestWeather();
        displayCurrentWeather(currentWeather);

        // Obtener datos históricos para el gráfico
        const weatherData = await API.getWeatherRange(startDate, endDate);
        console.log('Weather data for chart:', weatherData.length);
        createWeatherChart(weatherData);

    } catch (error) {
        console.error('Error loading weather data:', error);
        showNotification('Error al cargar datos del clima', 'error');
    } finally {
        loading.classList.add('hidden');
    }
}

function displayCurrentWeather(data) {
    const currentWeather = document.getElementById('currentWeather');

    const weatherIcon = getWeatherIcon(data.weather_main);

    currentWeather.innerHTML = `
        <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 text-center">
            <i class="fas ${weatherIcon} text-4xl text-blue-600 mb-2"></i>
            <p class="text-gray-600 text-sm font-medium">${data.city}, ${data.country}</p>
            <p class="text-3xl font-bold text-gray-800">${formatNumber(data.temperature, 1)}°C</p>
            <p class="text-gray-500 text-xs mt-1">${data.weather_description}</p>
        </div>

        <div class="bg-gray-50 rounded-lg p-4">
            <div class="flex items-center justify-between mb-2">
                <span class="text-gray-600 text-sm">Sensación térmica</span>
                <span class="font-semibold text-gray-800">${formatNumber(data.feels_like, 1)}°C</span>
            </div>
            <div class="flex items-center justify-between mb-2">
                <span class="text-gray-600 text-sm">Humedad</span>
                <span class="font-semibold text-gray-800">${data.humidity}%</span>
            </div>
            <div class="flex items-center justify-between">
                <span class="text-gray-600 text-sm">Presión</span>
                <span class="font-semibold text-gray-800">${data.pressure} hPa</span>
            </div>
        </div>

        <div class="bg-gray-50 rounded-lg p-4">
            <div class="flex items-center justify-between mb-2">
                <span class="text-gray-600 text-sm">Viento</span>
                <span class="font-semibold text-gray-800">${formatNumber(data.wind_speed, 1)} m/s</span>
            </div>
            <div class="flex items-center justify-between mb-2">
                <span class="text-gray-600 text-sm">Nubosidad</span>
                <span class="font-semibold text-gray-800">${data.clouds}%</span>
            </div>
            <div class="flex items-center justify-between">
                <span class="text-gray-600 text-sm">Temp. Mín/Máx</span>
                <span class="font-semibold text-gray-800">${formatNumber(data.temp_min, 1)}° / ${formatNumber(data.temp_max, 1)}°</span>
            </div>
        </div>

        <div class="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4 text-center flex flex-col justify-center">
            <p class="text-gray-600 text-xs mb-1">Última actualización</p>
            <p class="text-sm font-semibold text-gray-800">${formatDateTime(data.date)}</p>
        </div>
    `;
}

function getWeatherIcon(weatherMain) {
    const icons = {
        'Clear': 'fa-sun',
        'Clouds': 'fa-cloud',
        'Rain': 'fa-cloud-rain',
        'Drizzle': 'fa-cloud-rain',
        'Thunderstorm': 'fa-bolt',
        'Snow': 'fa-snowflake',
        'Mist': 'fa-smog',
        'Fog': 'fa-smog'
    };
    return icons[weatherMain] || 'fa-cloud';
}

// ==================== CRYPTO SECTION ====================
async function loadCryptoData(startDate, endDate) {
    const loading = document.getElementById('cryptoLoading');
    loading.classList.remove('hidden');

    try {
        // Obtener datos actuales
        const currentCrypto = await API.getLatestCrypto();
        console.log('Current crypto data:', currentCrypto);
        displayCryptoCards(currentCrypto);

        // Obtener datos históricos para el gráfico
        const cryptoData = await API.getCryptoRange(startDate, endDate);
        console.log('Crypto data for chart:', cryptoData.length);
        createCryptoChart(cryptoData);

    } catch (error) {
        console.error('Error loading crypto data:', error);
        showNotification('Error al cargar datos de criptomonedas', 'error');
    } finally {
        loading.classList.add('hidden');
    }
}

function displayCryptoCards(data) {
    const cryptoCards = document.getElementById('cryptoCards');

    if (!data || data.length === 0) {
        cryptoCards.innerHTML = '<p class="col-span-full text-center text-gray-500">No hay datos disponibles</p>';
        return;
    }

    console.log('Displaying crypto cards, total data:', data.length);

    // LIMITAR A 6 CRIPTOS EXACTOS, ordenados por market cap rank
    const topCryptos = data
        .sort((a, b) => a.market_cap_rank - b.market_cap_rank)
        .slice(0, 6);

    console.log('Top 6 cryptos:', topCryptos.map(c => `${c.symbol}: $${c.current_price}`));

    // Limpiar contenedor
    cryptoCards.innerHTML = '';

    // Crear cada tarjeta individualmente para evitar problemas de scope
    topCryptos.forEach(cryptoData => {
        const isPositive = cryptoData.price_change_percentage_24h > 0;
        const changeColor = isPositive ? 'text-green-600' : 'text-red-600';
        const changeBg = isPositive ? 'bg-green-100' : 'bg-red-100';
        const changeIcon = isPositive ? 'fa-arrow-up' : 'fa-arrow-down';

        const cardHTML = `
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-lg transition duration-300">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-2">
                        <div class="bg-yellow-100 rounded-full p-2">
                            <i class="fab fa-${getCryptoIcon(cryptoData.symbol)} text-yellow-600"></i>
                        </div>
                        <div>
                            <p class="font-bold text-gray-800">${cryptoData.symbol}</p>
                            <p class="text-xs text-gray-500">${cryptoData.name}</p>
                        </div>
                    </div>
                    <span class="text-xs ${changeBg} ${changeColor} px-2 py-1 rounded-full font-semibold">
                        #${cryptoData.market_cap_rank}
                    </span>
                </div>

                <div class="mb-3">
                    <p class="text-2xl font-bold text-gray-800">${formatCurrency(cryptoData.current_price)}</p>
                    <div class="flex items-center mt-1 ${changeColor}">
                        <i class="fas ${changeIcon} text-xs mr-1"></i>
                        <span class="text-sm font-semibold">${formatNumber(Math.abs(cryptoData.price_change_percentage_24h), 2)}%</span>
                    </div>
                </div>

                <div class="border-t pt-3 space-y-1">
                    <div class="flex justify-between text-xs">
                        <span class="text-gray-500">Market Cap</span>
                        <span class="font-semibold text-gray-700">${formatMarketCap(cryptoData.market_cap)}</span>
                    </div>
                    <div class="flex justify-between text-xs">
                        <span class="text-gray-500">Volumen 24h</span>
                        <span class="font-semibold text-gray-700">${formatMarketCap(cryptoData.total_volume)}</span>
                    </div>
                    <div class="flex justify-between text-xs">
                        <span class="text-gray-500">Alto/Bajo 24h</span>
                        <span class="font-semibold text-gray-700">${formatCurrency(cryptoData.high_24h).substring(0, 6)}/${formatCurrency(cryptoData.low_24h).substring(0, 6)}</span>
                    </div>
                </div>
            </div>
        `;

        cryptoCards.insertAdjacentHTML('beforeend', cardHTML);
    });
}

function formatMarketCap(value) {
    if (!value) return 'N/A';
    if (value >= 1e12) {
        return '$' + (value / 1e12).toFixed(2) + 'T';
    } else if (value >= 1e9) {
        return '$' + (value / 1e9).toFixed(2) + 'B';
    } else if (value >= 1e6) {
        return '$' + (value / 1e6).toFixed(2) + 'M';
    } else {
        return formatCurrency(value);
    }
}

function getCryptoIcon(symbol) {
    const icons = {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'ADA': 'cardano',
        'SOL': 'solana',
        'BNB': 'bnb',
        'XRP': 'coins'
    };
    return icons[symbol] || 'coins';
}

// ==================== TFL SECTION ====================
async function loadTflData() {
    const loading = document.getElementById('tflLoading');
    loading.classList.remove('hidden');

    try {
        const tflData = await API.getLatestTfl();
        console.log('TfL data:', tflData);
        displayTflStatus(tflData);
    } catch (error) {
        console.error('Error loading TfL data:', error);
        showNotification('Error al cargar datos de TfL', 'error');
    } finally {
        loading.classList.add('hidden');
    }
}

function displayTflStatus(data) {
    const tflContent = document.getElementById('tflContent');

    if (!data || data.length === 0) {
        tflContent.innerHTML = '<p class="col-span-full text-center text-gray-500">No hay datos disponibles</p>';
        return;
    }

    console.log('Displaying TfL, total data:', data.length);

    // LIMITAR A 8 LÍNEAS EXACTAS, ordenar por problemas primero
    const sortedData = data
        .sort((a, b) => {
            if (a.status_severity !== 10 && b.status_severity === 10) return -1;
            if (a.status_severity === 10 && b.status_severity !== 10) return 1;
            return a.status_severity - b.status_severity;
        })
        .slice(0, 8);

    console.log('Top 8 TfL lines:', sortedData.map(l => `${l.line_name}: ${l.status_severity_description}`));

    // Limpiar contenedor
    tflContent.innerHTML = '';

    // Crear cada tarjeta individualmente
    sortedData.forEach(lineData => {
        const statusColor = getStatusColor(lineData.status_severity);
        const statusIcon = getStatusIcon(lineData.status_severity);

        const cardHTML = `
            <div class="bg-white border-l-4 ${statusColor.border} rounded-lg p-4 hover:shadow-lg transition duration-300">
                <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center space-x-3">
                        <div class="${statusColor.bg} rounded-full p-2">
                            <i class="fas ${statusIcon} ${statusColor.text}"></i>
                        </div>
                        <div>
                            <h3 class="font-bold text-gray-800">${lineData.line_name}</h3>
                            <p class="text-xs text-gray-500">${lineData.line_id}</p>
                        </div>
                    </div>
                    <span class="text-xs ${statusColor.badge} px-3 py-1 rounded-full font-semibold">
                        ${lineData.status_severity_description}
                    </span>
                </div>
                ${lineData.reason ? `
                    <div class="mt-3 p-3 bg-gray-50 rounded">
                        <p class="text-sm text-gray-700"><i class="fas fa-info-circle mr-2"></i>${lineData.reason}</p>
                    </div>
                ` : ''}
            </div>
        `;

        tflContent.insertAdjacentHTML('beforeend', cardHTML);
    });
}

function getStatusColor(severity) {
    if (severity === 10) {
        return {
            border: 'border-green-500',
            bg: 'bg-green-100',
            text: 'text-green-600',
            badge: 'bg-green-100 text-green-800'
        };
    } else if (severity >= 6 && severity <= 9) {
        return {
            border: 'border-yellow-500',
            bg: 'bg-yellow-100',
            text: 'text-yellow-600',
            badge: 'bg-yellow-100 text-yellow-800'
        };
    } else {
        return {
            border: 'border-red-500',
            bg: 'bg-red-100',
            text: 'text-red-600',
            badge: 'bg-red-100 text-red-800'
        };
    }
}

function getStatusIcon(severity) {
    if (severity === 10) return 'fa-check-circle';
    if (severity >= 6) return 'fa-exclamation-triangle';
    return 'fa-times-circle';
}

// ==================== AUTO-REFRESH ====================
let autoRefreshInterval = null;

function startAutoRefresh() {
    if (CONFIG.AUTO_REFRESH_ENABLED) {
        console.log(`🔄 Auto-refresh activado cada ${CONFIG.AUTO_REFRESH_INTERVAL / 1000} segundos`);

        autoRefreshInterval = setInterval(async () => {
            console.log('🔄 Actualizando datos automáticamente...');
            await refreshAllData();
        }, CONFIG.AUTO_REFRESH_INTERVAL);
    }
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
        console.log('🛑 Auto-refresh detenido');
    }
}

// ==================== EVENT HANDLERS ====================
function applyDateRange() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    if (!startDate || !endDate) {
        showNotification('Por favor selecciona ambas fechas', 'warning');
        return;
    }

    if (new Date(endDate) < new Date(startDate)) {
        showNotification('La fecha final debe ser posterior a la fecha inicial', 'error');
        return;
    }

    refreshAllData();
}

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Inicializando Dashboard de Métricas...');

    initializeDates();
    await refreshAllData();
    startAutoRefresh();

    console.log('Dashboard cargado exitosamente!');
});

window.addEventListener('beforeunload', () => {
    stopAutoRefresh();
});
