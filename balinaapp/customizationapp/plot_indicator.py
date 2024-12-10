from .get_binance_data import get_binance_data
import plotly.graph_objs as go

def plot_indicator():
    # Binance verilerini çek
    data = get_binance_data()

    # Plotly mum grafiği oluştur
    fig = go.Figure(data=[go.Candlestick(
        x=data["time"],
        open=data["open"].astype(float),
        high=data["high"].astype(float),
        low=data["low"].astype(float),
        close=data["close"].astype(float),
        name="BTC/USDT"
    )])

    # Grafik düzenini güncelle
    fig.update_layout(
        title=None,
        xaxis_title=None,
        yaxis_title=None,
        template=None,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="black"),
        height=480,
        margin=dict(t=10, b=60, r=30, l=60),
        dragmode="pan",  # Sürükleme modu aktif
        xaxis_rangeslider_visible=False,  # Rangeslider'ı gizle
    )

    # Araç çubuğundan box select ve lasso select araçlarını kaldır ve scroll zoom'u aktif et
    config = {
        "modeBarButtonsToRemove": ["select2d", "lasso2d"],
        "scrollZoom": True  # Scroll zoom'u aktif et
    }

    # Grafiği HTML olarak render et
    chart_html = fig.to_html(full_html=False, config=config, include_plotlyjs=True)
    
    return chart_html
