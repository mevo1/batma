let trace;

// MAIN DATA
function downloadData(){
    const symbol = document.getElementById('dropdown1').value;
    const period = document.getElementById('dropdown2').value;
    const interval = document.getElementById('dropdown3').value;
    console.log(symbol, interval, period)
    fetch('/customization/api/graph/', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ symbol: symbol, interval: interval, period: period })
    })

    .then(response => {
        if (!response.ok) throw new Error(response.statusText);
        return response.json();
    })
    .then(data => {
        console.log(data);
        // Veriyi grafikte kullanmak için formatla
        trace = {
            x: data.time, // Zaman ekseni
            open: data.open.map(parseFloat), // Açılış değerleri
            high: data.high.map(parseFloat), // Yüksek değerler
            low: data.low.map(parseFloat), // Düşük değerler
            close: data.close.map(parseFloat), // Kapanış değerleri
            type: 'candlestick',
            name: 'main_graph' // DEĞİŞTİRİLECEKKK
        };
    
        // Grafik düzeni
        const layout = {
            title: null,
            xaxis: {
                title: null,
                rangeslider: { visible: false } // Rangeslider gizle
            },
            yaxis: {
                title: null
            },
            plot_bgcolor: "white",
            paper_bgcolor: "white",
            font: { color: "black" },
            height: 480,
            margin: { t: 10, b: 60, r: 30, l: 60 },
            dragmode: false, // Varsayılan olarak çizim modu kapalı
            newshape: {
                line: {
                    color: 'blue', // Çizilen çizgilerin rengi
                    width: 2 // Çizilen çizgilerin kalınlığı
                }
            }
        };
    
        // Konfigürasyon ayarları
        const config = {
            modeBarButtonsToAdd: [
                {
                    name: 'Çizgi Çizme Modu',
                    icon: Plotly.Icons.pencil, // Sol üstte gösterilecek ikon
                    click: function(gd) {
                        // Çizgi çizme modunu aktif/pasif yap
                        let currentMode = gd._fullLayout.dragmode;
                        Plotly.relayout(gd, { dragmode: currentMode === 'drawline' ? false : 'drawline' });
                    }
                },
                {
                    name: 'Çizgileri Kaldır',
                    icon: Plotly.Icons.trash, // Çöp kutusu ikonu
                    click: function(gd) {
                        // Çizgileri kaldır
                        Plotly.relayout(gd, { shapes: [] });
                    }
                }
            ],
            modeBarButtonsToRemove: ["select2d", "lasso2d"],
            scrollZoom: true, // Scroll zoom'u aktif et
            displayModeBar: true // Mod çubuğunu göster
        };
    
        // Grafiği oluştur ve container'a ekle
        Plotly.newPlot('chart-container', [trace], layout, config);
    })       
    .catch(error => {
        alert(`An error occurred: ${error.message}`);
    });

}

// INDICATOR VİSİBLE
function visibleIndicator(id,event){
    event.stopPropagation();
    
    fetch(`/customization/api/graph/${id}/`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({id})
    })
    .then(response => {
        if (!response.ok) throw new Error(response.statusText);
        return response.json();
    })
    .then(data => {
        console.log(data);
        // Yeni gelen result verisini içeren bir ek veri dizisi
        const resultTrace = {
            x: data.time,
            y: data.result, // Gelen result verisi y eksenine eklenir
            type: 'scatter',
            mode: 'lines',
            name: data.name // Göstergenin adını belirt
        };
    
        // Grafik düzeni
        const layout = {
            title: null,
            xaxis: {
                title: null,
                rangeslider: { visible: false } // Rangeslider gizle
            },
            yaxis: {
                title: null
            },
            plot_bgcolor: "white",
            paper_bgcolor: "white",
            font: { color: "black" },
            height: 480,
            margin: { t: 10, b: 60, r: 30, l: 60 },
            dragmode: false, // Varsayılan olarak çizim modu kapalı
            newshape: {
                line: {
                    color: 'blue', // Çizilen çizgilerin rengi
                    width: 2 // Çizilen çizgilerin kalınlığı
                }
            }
        };
    
        // Konfigürasyon ayarları
        const config = {
            modeBarButtonsToAdd: [
                {
                    name: 'Çizgi Çizme Modu',
                    icon: Plotly.Icons.pencil,
                    click: function(gd) {
                        let currentMode = gd._fullLayout.dragmode;
                        Plotly.relayout(gd, { dragmode: currentMode === 'drawline' ? false : 'drawline' });
                    }
                },
                {
                    name: 'Çizgileri Kaldır',
                    icon: Plotly.Icons.trash,
                    click: function(gd) {
                        Plotly.relayout(gd, { shapes: [] });
                    }
                }
            ],
            modeBarButtonsToRemove: ["select2d", "lasso2d"],
            scrollZoom: true,
            displayModeBar: true
        };
    
        // Grafiği oluştur ve container'a ekle
        Plotly.newPlot('chart-container', [trace,resultTrace], layout, config);
    })
    .catch(error => {
        alert(`An error occurred: ${error.message}`);
    });
}