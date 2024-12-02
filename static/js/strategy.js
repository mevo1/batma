const saveButton = document.getElementById('save-btn');
const strategyNameInput = document.getElementById('strategy-name');
const codeArea = document.getElementById('code-area');
const strategiesDiv = document.getElementById('strategies');

// Stratejileri Yükleme (Sayfa Açıldığında)
document.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/api/strategies/');
    const strategies = await response.json();

    strategies.forEach(strategy => {
        addStrategyToList(strategy.name, strategy.id);
    });
});


// Kaydetme İşlevi
saveButton.addEventListener('click', async () => {
    const strategyName = strategyNameInput.value.trim();
    const code = codeArea.value;

    if (!strategyName) {
        alert('Lütfen bir strateji adı girin!');
        return;
    }

    const response = await fetch('/api/strategies/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: strategyName, code: code }),
    });

    if (response.ok) {
        const strategy = await response.json();
        addStrategyToList(strategy.name, strategy.id);
        alert(`"${strategyName}" kaydedildi!`);
    } else {
        alert('Strateji kaydedilirken bir hata oluştu.');
    }
});


// Strateji Listeye Ekleme
function addStrategyToList(strategyName, strategyId) {
    const strategyItem = document.createElement('div');
    strategyItem.className = 'strategy-item';

    const strategyText = document.createElement('span');
    strategyText.textContent = strategyName;
    strategyText.addEventListener('click', async () => {
        const response = await fetch(`/api/strategies/${strategyId}/`);
        const strategy = await response.json();

        strategyNameInput.value = strategy.name;
        codeArea.value = strategy.code;
    });

    const deleteButton = document.createElement('button');
    deleteButton.className = 'delete-btn';
    deleteButton.textContent = 'Sil';
    deleteButton.addEventListener('click', async () => {
        if (confirm(`"${strategyName}" adlı stratejiyi silmek istediğinize emin misiniz?`)) {
            const response = await fetch(`/api/strategies/${strategyId}/`, { method: 'DELETE' });
            if (response.ok) {
                strategiesDiv.removeChild(strategyItem);
            }
        }
    });

    strategyItem.appendChild(strategyText);
    strategyItem.appendChild(deleteButton);
    strategiesDiv.appendChild(strategyItem);
}
