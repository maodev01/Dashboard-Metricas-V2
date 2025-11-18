// Módulo de API para comunicación con el backend

const API = {
    // Función base para hacer peticiones
    async request(endpoint, options = {}) {
        try {
            const url = `${CONFIG.API_BASE_URL}${endpoint}`;
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    },

    // ==================== WEATHER ====================
    async getLatestWeather() {
        return await this.request('/weather/latest');
    },

    async getDailyWeather(date) {
        const query = date ? `?target_date=${date}` : '';
        return await this.request(`/weather/daily${query}`);
    },

    async getWeatherRange(startDate, endDate) {
        return await this.request(`/weather/range?start_date=${startDate}&end_date=${endDate}`);
    },

    async collectWeather(city = null, country = null) {
        let url = '/weather/collect';
        const params = new URLSearchParams();
        if (city) params.append('city', city);
        if (country) params.append('country', country);
        if (params.toString()) url += `?${params.toString()}`;

        return await this.request(url, { method: 'POST' });
    },

    // ==================== CRYPTO ====================
    async getLatestCrypto() {
        return await this.request('/crypto/latest');
    },

    async getDailyCrypto(date, symbol = null) {
        let url = '/crypto/daily';
        const params = new URLSearchParams();
        if (date) params.append('target_date', date);
        if (symbol) params.append('symbol', symbol);
        if (params.toString()) url += `?${params.toString()}`;

        return await this.request(url);
    },

    async getCryptoRange(startDate, endDate, symbol = null) {
        let url = `/crypto/range?start_date=${startDate}&end_date=${endDate}`;
        if (symbol) url += `&symbol=${symbol}`;
        return await this.request(url);
    },

    async collectCrypto(cryptoIds = null) {
        let url = '/crypto/collect';
        if (cryptoIds && cryptoIds.length > 0) {
            const params = cryptoIds.map(id => `crypto_ids=${id}`).join('&');
            url += `?${params}`;
        }
        return await this.request(url, { method: 'POST' });
    },

// ==================== TFL ====================
    async getLatestTfl() {
        return await this.request('/tfl/latest');
    },

    async getTflLine(lineId) {
        return await this.request(`/tfl/line/${lineId}`);
    },

    async getTflRange(startDate, endDate, lineId = null) {
        let url = `/tfl/range?start_date=${startDate}&end_date=${endDate}`;
        if (lineId) url += `&line_id=${lineId}`;
        return await this.request(url);
    },

    async collectTfl() {
        return await this.request('/tfl/collect', { method: 'POST' });
    },

    async getBikePoints() {
        return await this.request('/tfl/bikes');
    },

    // ==================== STATS ====================
    async getStatsSummary() {
        return await this.request('/stats/summary');
    }
};

// Funciones helper para colección de datos
async function collectAllData() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(btn => btn.disabled = true);

    try {
        showNotification('Colectando datos...', 'info');

        const results = await Promise.allSettled([
            API.collectWeather(),
            API.collectCrypto(),
            API.collectTfl()
        ]);

        const successful = results.filter(r => r.status === 'fulfilled').length;
        const failed = results.filter(r => r.status === 'rejected').length;

        if (failed === 0) {
            showNotification('Todos los datos colectados exitosamente!', 'success');
        } else if (successful > 0) {
            showNotification(`${successful} colecciones exitosas, ${failed} fallaron`, 'warning');
        } else {
            showNotification('Error al colectar datos', 'error');
        }

        await refreshAllData();

    } catch (error) {
        console.error('Error collecting data:', error);
        showNotification('Error al colectar datos', 'error');
    } finally {
        buttons.forEach(btn => btn.disabled = false);
    }
}

let refreshLock = false;
// Función para refrescar todos los datos
async function refreshAllData() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    await Promise.all([
        loadWeatherData(startDate, endDate),
        loadCryptoData(startDate, endDate),
        loadTflData(),
        loadStats()
    ]);
}
