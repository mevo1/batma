from django.shortcuts import render, redirect
from .forms import MyForm, IndicatorForm
from .models import Indicator
from django.http import HttpResponseForbidden
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

def indicator_create(request):
    if request.method == 'POST':
        form = IndicatorForm(request.POST)
        if form.is_valid():
            indicator = form.save(commit=False)
            indicator.user = request.user  # İndikatörü oluşturan kullanıcıyı ekle
            indicator.save()
            return redirect('indicator_list')  # Form gönderildiğinde yönlendirme yapılacak bir sayfa
    else:
        form = IndicatorForm()

    return render(request, 'indicator_form.html', {'form': form})

def indicator_list(request):
    indicators = Indicator.objects.filter(user=request.user)  # Tüm Indicator kayıtlarını getir
    return render(request, 'indicator_list.html', {'indicators': indicators})

def edit_indicator(request, indicator_id):
    indicator = Indicator.objects.get(id=indicator_id)
    if indicator.user != request.user:
        return HttpResponseForbidden()