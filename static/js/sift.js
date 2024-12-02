document.addEventListener('DOMContentLoaded', () => {
  const cryptoSelect = document.getElementById('crypto-select');
  const cryptoList = document.getElementById('crypto-list');

  cryptoSelect.addEventListener('change', () => {
      const selectedValue = cryptoSelect.value;
      const existingItem = [...cryptoList.children].find(
          (item) => item.dataset.value === selectedValue
      );

      if (!existingItem) {
          const listItem = document.createElement('li');
          listItem.dataset.value = selectedValue;
          listItem.innerHTML = `
              ${selectedValue.toUpperCase()} 
              <button class="remove-btn">Sil</button>
          `;

          cryptoList.appendChild(listItem);

          // Remove button functionality
          listItem.querySelector('.remove-btn').addEventListener('click', () => {
              cryptoList.removeChild(listItem);
          });
      }
  });
});
