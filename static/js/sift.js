document.addEventListener("DOMContentLoaded", () => {
    // Dropdown toggle
    function setupDropdown(buttonId, menuId) {
      const button = document.getElementById(buttonId);
      const menu = document.getElementById(menuId);
  
      button.addEventListener("click", () => {
        menu.classList.toggle("hidden");
      });
  
      document.addEventListener("click", (e) => {
        if (!button.contains(e.target) && !menu.contains(e.target)) {
          menu.classList.add("hidden");
        }
      });
    }
  
    // Coin selection logic
    const coinButton = document.getElementById("coin-button");
    const coinList = document.getElementById("coin-list");
    const selectedCoins = document.getElementById("selected-coins");
  
    coinList.addEventListener("click", (e) => {
      if (e.target.tagName === "LI") {
        const coin = e.target.dataset.value;
        addSelection(selectedCoins, coin);
      }
    });
  
    // Strategy selection logic
    const strategyList = document.getElementById("strategy-list");
    const selectedStrategies = document.getElementById("selected-strategies");
  
    strategyList.addEventListener("click", (e) => {
      if (e.target.tagName === "LI") {
        const strategy = e.target.dataset.value;
        addSelection(selectedStrategies, strategy);
      }
    });
  
    // Timeframe selection logic
    const timeframeList = document.getElementById("timeframe-list");
    const selectedTimeframes = document.getElementById("selected-timeframes");
  
    timeframeList.addEventListener("click", (e) => {
      if (e.target.tagName === "LI") {
        const timeframe = e.target.dataset.value;
        addSelection(selectedTimeframes, timeframe);
      }
    });
  
    // Dropdown setup
    setupDropdown("coin-button", "coin-list");
    setupDropdown("strategy-button", "strategy-list");
    setupDropdown("timeframe-button", "timeframe-list");
  
    // Genel fonksiyon: Seçim ekleme ve silme
    function addSelection(container, value) {
      const existingItems = Array.from(container.children).map(
        (child) => child.textContent
      );
  
      if (!existingItems.includes(value)) {
        const span = document.createElement("span");
        span.textContent = value;
        span.classList.add("selected-item");
        span.addEventListener("click", () => container.removeChild(span)); // Tıklanınca silinir
        container.appendChild(span);
      }
    }
  });
  