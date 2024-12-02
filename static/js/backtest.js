document.getElementById('backtestBtn').addEventListener('click', () => {
    const crypto = document.getElementById('crypto').value;
    const strategy = document.getElementById('strategy').value;
    const period = document.getElementById('period').value;
    const commission = document.getElementById('commission').value;
  
    console.log(`Kripto Para: ${crypto}`);
    console.log(`Strateji: ${strategy}`);
    console.log(`Periyot: ${period}`);
    console.log(`Komisyon Oranı: ${commission}`);

    // Şimdilik sadece konsola yazdırıyor. Backtest işlemi burada yapılabilir.
    alert('Backtest başlatıldı!');
  });
  
  