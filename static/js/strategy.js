const saveButton = document.getElementById('save-btn');
const strategyNameInput = document.getElementById('strategy-name');
const codeArea = document.getElementById('code-area');
const strategiesDiv = document.getElementById('strategies');

// Stratejileri Yükleme (Sayfa Açıldığında)
document.addEventListener('DOMContentLoaded', () => {
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        addStrategyToList(key);
    }
});

// Kaydetme İşlevi
saveButton.addEventListener('click', () => {
    const strategyName = strategyNameInput.value.trim();
    if (!strategyName) {
        alert('Lütfen bir strateji adı girin!');
        return;
    }
    if (!localStorage.getItem(strategyName)) {
        addStrategyToList(strategyName);
    }
    localStorage.setItem(strategyName, codeArea.value);
    alert(`"${strategyName}" kaydedildi!`);
});

// Strateji Listeye Ekleme
function addStrategyToList(strategyName) {
    const strategyItem = document.createElement('div');
    strategyItem.className = 'strategy-item';

    const strategyText = document.createElement('span');
    strategyText.textContent = strategyName;
    strategyText.addEventListener('click', () => {
        strategyNameInput.value = strategyName;
        codeArea.value = localStorage.getItem(strategyName) || '';
    });

    const deleteButton = document.createElement('button');
    deleteButton.className = 'delete-btn';
    deleteButton.textContent = 'Sil';
    deleteButton.addEventListener('click', () => {
        if (confirm(`"${strategyName}" adlı stratejiyi silmek istediğinize emin misiniz?`)) {
            localStorage.removeItem(strategyName);
            strategiesDiv.removeChild(strategyItem);
        }
    });

    strategyItem.appendChild(strategyText);
    strategyItem.appendChild(deleteButton);
    strategiesDiv.appendChild(strategyItem);
}
