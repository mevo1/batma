document.addEventListener("DOMContentLoaded", () => {
  fetch('/api/backtest-results/')
      .then(response => response.json())
      .then(data => {
          document.getElementById('totalPL').textContent = `${data.total_pl} %`;
          document.getElementById('totalTrades').textContent = data.total_trades;
          document.getElementById('winningTrades').textContent = data.winning_trades;
          document.getElementById('losingTrades').textContent = data.losing_trades;
          document.getElementById('successRate').textContent = `${data.success_rate} %`;
          document.getElementById('maxProfit').textContent = `${data.max_profit} %`;
          document.getElementById('maxLoss').textContent = `${data.max_loss} %`;
          document.getElementById('avgDuration').textContent = `${data.avg_duration} gün`;
          document.getElementById('strategyDuration').textContent = `${data.strategy_duration} gün`;
          document.getElementById('rating').textContent = data.rating;
      })
      .catch(error => console.error('Veriler alınırken bir hata oluştu:', error));
});
