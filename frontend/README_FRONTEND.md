# Frontend - Dashboard de Métricas

Frontend completo con HTML, Chart.js y Tailwind CSS para visualizar métricas de clima, criptomonedas y NASA APOD.

## 📁 Estructura del Proyecto

```
frontend/
├── index.html           # Página principal
├── js/
│   ├── config.js       # Configuración y utilidades
│   ├── api.js          # Comunicación con el backend
│   ├── charts.js       # Gráficos con Chart.js
│   └── dashboard.js    # Lógica principal del dashboard
└── README.md           # Esta documentación
```

## 🎨 Características

### ✨ Interfaz de Usuario
- **Diseño moderno** con Tailwind CSS
- **Responsive design** - funciona en desktop, tablet y móvil
- **Animaciones suaves** en transiciones y hover effects
- **Iconos de Font Awesome** para mejor UX
- **Notificaciones toast** para feedback del usuario

### 📊 Visualizaciones
- **Gráficos interactivos** con Chart.js
- **Datos en tiempo real** del clima actual
- **Cards de criptomonedas** con precios y cambios
- **NASA APOD** con imágenes y explicaciones
- **Estadísticas resumidas** en tarjetas coloridas

### 🔧 Funcionalidades
- **Selector de rango de fechas** para análisis histórico
- **Botón de actualización** para refrescar datos
- **Botón de colección** para obtener nuevos datos
- **Gráficos de múltiples líneas** para comparación
- **Tooltips informativos** en todos los gráficos

## 🚀 Instalación y Uso

### Opción 1: Servidor Local Simple

```bash
# Si tienes Python instalado
cd frontend
python -m http.server 8080

# O con Node.js
npx http-server -p 8080
```

Luego abre: http://localhost:8080

### Opción 2: Con Nginx (Producción)

```bash
# Copiar archivos al directorio de Nginx
sudo cp -r frontend/* /var/www/html/

# Reiniciar Nginx
sudo systemctl restart nginx
```

### Opción 3: Live Server (VS Code)

1. Instalar extensión "Live Server" en VS Code
2. Click derecho en `index.html`
3. Seleccionar "Open with Live Server"

## ⚙️ Configuración

Editar `js/config.js` para cambiar la URL de la API:

```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000/api',  // Cambiar según tu backend
    // ... otras configuraciones
};
```

### Configuraciones Disponibles

- **API_BASE_URL**: URL del backend
- **CHART_COLORS**: Paleta de colores para gráficos
- **CRYPTO_SYMBOLS**: Símbolos de criptomonedas a mostrar
- **DEFAULT_DAYS_RANGE**: Días por defecto en gráficos (7)

## 📱 Componentes del Dashboard

### 1. Header
- Título y descripción
- Botón de actualización
- Botón de colección de datos

### 2. Estadísticas Resumidas
Tres tarjetas con:
- Total de registros del clima
- Total de registros de criptomonedas
- Total de registros de NASA
- Última fecha de actualización de cada uno

### 3. Selector de Rango de Fechas
- Input de fecha inicial
- Input de fecha final
- Botón de búsqueda

### 4. Sección de Clima
- **Tarjetas actuales**: Temperatura, sensación térmica, humedad, presión, viento, nubosidad
- **Gráfico de líneas**: Temperatura, humedad y velocidad del viento en el tiempo

### 5. Sección de Criptomonedas
- **Cards individuales**: Precio actual, cambio 24h, market cap, volumen
- **Gráfico de líneas**: Evolución de precios de múltiples criptos

### 6. Sección de NASA APOD
- **Imagen/Video del día**: Con modal para ver en HD
- **Título y fecha**: Del APOD
- **Explicación completa**: Descripción de la imagen
- **Botones**: Ver HD y abrir original

## 🎨 Personalización de Estilos

### Colores Principales
```css
Purple Primary: #667eea
Purple Secondary: #764ba2
Blue: #3b82f6
Yellow: #fbbf24
Green: #22c55e
Red: #ef4444
```

### Modificar Colores de Gráficos
Editar en `js/config.js`:
```javascript
CHART_COLORS: {
    primary: 'rgba(102, 126, 234, 1)',
    primaryLight: 'rgba(102, 126, 234, 0.2)',
    // ... más colores
}
```

## 🔌 Funciones Principales

### API Calls
```javascript
// Obtener datos del clima
await API.getLatestWeather();
await API.getWeatherRange(startDate, endDate);

// Obtener datos de criptomonedas
await API.getLatestCrypto();
await API.getCryptoRange(startDate, endDate);

// Obtener datos de NASA
await API.getLatestNasa();

// Colectar nuevos datos
await collectAllData();
```

### Actualización de Datos
```javascript
// Refrescar todo el dashboard
await refreshAllData();

// Aplicar nuevo rango de fechas
applyDateRange();
```

### Notificaciones
```javascript
// Mostrar notificación
showNotification('Mensaje', 'success'); // success, error, warning, info
```

## 📊 Tipos de Gráficos

### Gráfico del Clima (Múltiples Ejes Y)
- **Eje Y izquierdo**: Temperatura (°C)
- **Eje Y derecho**: Humedad (%) y Viento (m/s)
- **Tipo**: Líneas con relleno

### Gráfico de Criptomonedas
- **Eje Y**: Precio (USD)
- **Tipo**: Líneas múltiples (una por cripto)
- **Tooltip**: Precio formateado en USD

## 🐛 Solución de Problemas

### Error: "Failed to fetch"
- Verificar que el backend esté corriendo en `http://localhost:8000`
- Verificar CORS en el backend
- Revisar la URL en `config.js`

### Gráficos no se muestran
- Verificar que Chart.js esté cargado correctamente
- Revisar la consola del navegador por errores
- Verificar que haya datos disponibles

### Fechas no funcionan
- Verificar formato de fecha (YYYY-MM-DD)
- Asegurarse que la fecha final sea posterior a la inicial

## 📱 Responsive Breakpoints

- **Mobile**: < 768px (stack vertical)
- **Tablet**: 768px - 1024px (2 columnas)
- **Desktop**: > 1024px (4 columnas)

## 🔐 Seguridad

- No hay autenticación implementada (agregar según necesidad)
- Todas las llamadas son a través de la API pública del backend
- No se almacenan datos sensibles en el frontend

## 🚀 Optimizaciones Implementadas

- **Lazy loading**: Carga de datos bajo demanda
- **Debouncing**: En búsquedas y actualizaciones
- **Caché de gráficos**: Destruye y recrea solo cuando es necesario
- **Animaciones CSS**: Usa transform para mejor performance

## 📝 Próximos Pasos

1. ✅ Frontend completo funcionando
2. ⏭️ Agregar filtros avanzados
3. ⏭️ Exportar datos a CSV/PDF
4. ⏭️ Modo oscuro
5. ⏭️ PWA para uso offline

## 🤝 Integración con Backend

El frontend espera los siguientes endpoints del backend:

```
GET  /api/weather/latest
GET  /api/weather/range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
GET  /api/crypto/latest
GET  /api/crypto/range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
GET  /api/nasa/latest
GET  /api/stats/summary
POST /api/weather/collect
POST /api/crypto/collect
POST /api/nasa/collect
```

## 📄 Licencia

MIT

---

**Nota**: Asegúrate de que el backend esté corriendo antes de usar el frontend.