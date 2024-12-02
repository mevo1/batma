const binanceAPI = 'https://api.binance.com/api/v3/klines';
const symbolAPI = 'https://api.binance.com/api/v3/ticker/price';
let currentSymbol = 'BTCUSDT'; // Varsayılan Bitcoin/USDT

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

// Binance API'den veri çek ve grafiği güncelle
async function fetchData(symbol = currentSymbol) {
    try {
        const response = await axios.get(binanceAPI, {
            params: { symbol, interval: '4h', limit: 600 },
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

// Kripto para listesi oluştur
async function populateCryptoSelector() {
    try {
        const response = await axios.get(symbolAPI);
        const cryptoSelector = document.getElementById('crypto-selector');

        response.data
            .filter((coin) => coin.symbol.endsWith('USDT')) // Sadece USDT çiftlerini al
            .slice(0, 200) // İlk 200 kripto para
            .forEach((coin) => {
                const option = document.createElement('option');
                option.value = coin.symbol;
                option.textContent = coin.symbol;
                cryptoSelector.appendChild(option);
            });

        cryptoSelector.addEventListener('change', (e) => {
            currentSymbol = e.target.value;
            fetchData(currentSymbol); // Seçilen kripto para için grafiği güncelle
        });
    } catch (error) {
        console.error('Kripto para listesi alınamadı:', error);
    }
}

populateCryptoSelector(); // Seçici menüyü doldur
fetchData(); // Varsayılan grafiği yükle
setInterval(() => fetchData(currentSymbol), 60000); // Grafiği güncelle

