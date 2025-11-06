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
            
            <div class="bg-gradient-to-br from-red-500 to-red-600 rounded-lg shadow-lg p-6 text-white card-hover transition duration-300">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-red-100 text-sm font-medium">NASA APOD</p>
                        <p class="text-3xl font-bold mt-2">${stats.total_records.nasa}</p>
                        <p class="text-red-100 text-xs mt-2">
                            ${stats.latest_dates.nasa ? 'Último: ' + formatDateTime(stats.latest_dates.nasa) : 'Sin datos'}
                        </p>
                    </div>
                    <div class="bg-red-400 bg-opacity-30 rounded-full p-4">
                        <i class="fas fa-rocket text-4xl"></i>
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
        
        // Obtener datos históricos
        const weatherData = await API.getWeatherRange(startDate, endDate);
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
        displayCryptoCards(currentCrypto);
        
        // Obtener datos históricos
        const cryptoData = await API.getCryptoRange(startDate, endDate);
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
        cryptoCards.innerHTML = '<p class="col-span-4 text-center text-gray-500">No hay datos disponibles</p>';
        return;
    }
    
    cryptoCards.innerHTML = data.map(crypto => {
        const isPositive = crypto.price_change_percentage_24h > 0;
        const changeColor = isPositive ? 'text-green-600' : 'text-red-600';
        const changeBg = isPositive ? 'bg-green-100' : 'bg-red-100';
        const changeIcon = isPositive ? 'fa-arrow-up' : 'fa-arrow-down';
        
        return `
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-lg transition duration-300">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-2">
                        <div class="bg-yellow-100 rounded-full p-2">
                            <i class="fab fa-${getCryptoIcon(crypto.symbol)} text-yellow-600"></i>
                        </div>
                        <div>
                            <p class="font-bold text-gray-800">${crypto.symbol}</p>
                            <p class="text-xs text-gray-500">${crypto.name}</p>
                        </div>
                    </div>
                    <span class="text-xs ${changeBg} ${changeColor} px-2 py-1 rounded-full font-semibold">
                        #${crypto.market_cap_rank}
                    </span>
                </div>
                
                <div class="mb-3">
                    <p class="text-2xl font-bold text-gray-800">${formatCurrency(crypto.current_price)}</p>
                    <div class="flex items-center mt-1 ${changeColor}">
                        <i class="fas ${changeIcon} text-xs mr-1"></i>
                        <span class="text-sm font-semibold">${formatNumber(Math.abs(crypto.price_change_percentage_24h), 2)}%</span>
                    </div>
                </div>
                
                <div class="border-t pt-3 space-y-1">
                    <div class="flex justify-between text-xs">
                        <span class="text-gray-500">Market Cap</span>
                        <span class="font-semibold text-gray-700">${formatCurrency(crypto.market_cap, 'USD').slice(0, -3)}M</span>
                    </div>
                    <div class="flex justify-between text-xs">
                        <span class="text-gray-500">Volumen 24h</span>
                        <span class="font-semibold text-gray-700">${formatCurrency(crypto.total_volume, 'USD').slice(0, -3)}M</span>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function getCryptoIcon(symbol) {
    const icons = {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'ADA': 'cardano',
        'SOL': 'solana',
        'BNB': 'bnb'
    };
    return icons[symbol] || 'coins';
}

// ==================== NASA SECTION ====================
async function loadNasaData() {
    const loading = document.getElementById('nasaLoading');
    loading.classList.remove('hidden');
    
    try {
        const nasaData = await API.getLatestNasa();
        displayNasaContent(nasaData);
    } catch (error) {
        console.error('Error loading NASA data:', error);
        showNotification('Error al cargar datos de NASA', 'error');
    } finally {
        loading.classList.add('hidden');
    }
}

function displayNasaContent(data) {
    const nasaContent = document.getElementById('nasaContent');
    
    if (!data) {
        nasaContent.innerHTML = '<p class="col-span-2 text-center text-gray-500">No hay datos disponibles</p>';
        return;
    }
    
    const mediaHtml = data.media_type === 'image' 
        ? `<img src="${data.url}" alt="${data.title}" class="w-full h-full object-cover rounded-lg cursor-pointer hover:opacity-90 transition" onclick="window.open('${data.hdurl || data.url}', '_blank')">`
        : `<iframe src="${data.url}" class="w-full h-full rounded-lg" frameborder="0" allowfullscreen></iframe>`;
    
    nasaContent.innerHTML = `
        <div class="relative h-96 bg-black rounded-lg overflow-hidden">
            ${mediaHtml}
            ${data.copyright ? `<div class="absolute bottom-2 right-2 bg-black bg-opacity-50 text-white text-xs px-2 py-1 rounded">© ${data.copyright}</div>` : ''}
        </div>
        
        <div class="space-y-4">
            <div>
                <h3 class="text-2xl font-bold text-gray-800 mb-2">${data.title}</h3>
                <p class="text-sm text-gray-500 mb-4">
                    <i class="far fa-calendar mr-2"></i>${data.apod_date}
                </p>
                <p class="text-gray-700 leading-relaxed">${data.explanation}</p>
            </div>
            
            <div class="flex space-x-3">
                ${data.hdurl ? `
                    <a href="${data.hdurl}" target="_blank" class="flex-1 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition text-center flex items-center justify-center space-x-2">
                        <i class="fas fa-expand"></i>
                        <span>Ver HD</span>
                    </a>
                ` : ''}
                <a href="${data.url}" target="_blank" class="flex-1 bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition text-center flex items-center justify-center space-x-2">
                    <i class="fas fa-external-link-alt"></i>
                    <span>Abrir Original</span>
                </a>
            </div>
        </div>
    `;
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
    
    // Inicializar fechas
    initializeDates();
    
    // Cargar todos los datos
    await refreshAllData();
    
    console.log('Dashboard cargado exitosamente!');
});