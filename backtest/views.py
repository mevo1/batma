from django.shortcuts import render, redirect
from .forms import MyForm, IndicatorForm,StrategyForm
from .models import Indicator,Strategy
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
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
        form = IndicatorForm(request.POST, initial={'user': request.user})  # Pass the user in initial data
        if form.is_valid():
            indicator = form.save(commit=False)
            indicator.user = request.user  # İndikatörü oluşturan kullanıcıyı ekle
            indicator.save()
            return redirect('indicator_list') # Form gönderildiğinde yönlendirme yapılacak bir sayfa
    else:
        form = IndicatorForm(initial={'user': request.user})

    return render(request, 'indicator_form.html', {'form': form})

def indicator_list(request):
    indicators = Indicator.objects.filter(user=request.user)  # Tüm Indicator kayıtlarını getir
    return render(request, 'indicator_list.html', {'indicators': indicators})

def edit_indicator(request, indicator_id):
    indicator = Indicator.objects.get(id=indicator_id)
    if indicator.user != request.user:
        return HttpResponseForbidden()

def ozellikler_sayfasi(request):
    return render (request, 'ozellikler.html')

def mainmenu(request):
    user = User.objects.get(username = 'bilal_bostan')
    context = {
        'user': user,
    }
    return render (request, 'mainmenu.html', context)

def strategy(request):
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            form.save()  # Veri tabanına kaydediyoruz
            return redirect('strategy')  # Başarılı olursa tekrar aynı sayfaya dön
    else:
        form = StrategyForm()
    
    # Tüm stratejileri listelemek için
    strategies = Strategy.objects.all()
    
    return render(request, 'strategy.html', {'form': form, 'strategies': strategies})

