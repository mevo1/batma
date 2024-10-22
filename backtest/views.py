from django.shortcuts import render
from .forms import MyForm
import yfinance as yf

coinler = ["bitcoin","ethereum","pepe"]
range = ["1 yıl", "1 ay", "1 hafta"]

def home(request):
    data = {
        "coins": coinler,
        "ranges": range
    }
    return render(request, "index.html", data)

def backtest(request):
    return render(request, "backtest.html")

def showData(request):
    # Veri çekme
    stock = yf.Ticker("BTC-USD")
    stock_info = stock.history(period="5d")

    # DateTimeIndex'i stringe çevirme
    stock_info.index = stock_info.index.strftime('%Y-%m-%d')

    # Veriyi şablona gönderirken .to_dict() kullanıyoruz
    context = {
        'stock_info': stock_info.to_dict(orient="index")  # 'index' verileri {tarih: {...}} olarak verir
    }
    print(context)
    print(type(context))

    return render(request, "showData.html", context)

def script(request):

    output_text = ''
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            output_text = form.cleaned_data['input_text']
    else:
        form = MyForm()

    return render(request, "script.html", {'form': form, 'output_text': output_text})