// Binance API'sinden fiyat verisi çekme
const binanceAPI = 'https://api.binance.com/api/v3/klines';
const symbol = 'BTCUSDT'; // Bitcoin/USDT çifti
const interval = '1d'; // periyot

// Grafik oluşturma
const chartContainer = document.getElementById('chart-container');
const chart = LightweightCharts.createChart(chartContainer, {
    width: chartContainer.clientWidth,
    height: chartContainer.clientHeight,
    layout: {
        backgroundColor: '#ffffff',
        textColor: '#333',
    },
    grid: {
        vertLines: { color: '#e1e1e1' },
        horzLines: { color: '#e1e1e1' },
    },
    crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
    },
    rightPriceScale: {
        borderColor: '#cccccc',
    },
    timeScale: {
        borderColor: '#cccccc',
    },
});
const candleSeries = chart.addCandlestickSeries();

// Binance API'den veri çek ve grafiğe yükle
async function fetchData() {
    try {
        const response = await axios.get(binanceAPI, {
            params: { symbol, interval, limit: 500 },
        });
        const data = response.data.map(([time, open, high, low, close]) => ({
            time: time / 1000,
            open: parseFloat(open),
            high: parseFloat(high),
            low: parseFloat(low),
            close: parseFloat(close),
        }));
        candleSeries.setData(data);
    } catch (error) {
        console.error('Veri alınamadı:', error);
    }
}

fetchData();
setInterval(fetchData, 60000); // Her dakika veriyi güncelle
