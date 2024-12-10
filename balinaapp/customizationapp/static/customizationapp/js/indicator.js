document.addEventListener("DOMContentLoaded", loadIndicators);
function loadIndicators() {
    fetch(indicatorListUrl)
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById("indicatorList");
            list.innerHTML = "";
            data.forEach((indicator, index) => {
                list.innerHTML +=  `
                <li data-id="${indicator.id}" onclick="editIndicator(${indicator.id})">
                    <a>
                        <strong>${index + 1}.</strong> <!-- artan numara -->
                        <i class="fas fa-chart-line"></i> ${indicator.title}
                    </a>
                    <button id="visibleBtn-${indicator.id}" class="visible-btn" onclick="visibleIndicator(${indicator.id}, event)">Visible</button>
                    <button id="deleteBtn-${indicator.id}" class="delete-btn" onclick="deleteIndicator(${indicator.id}, event)">Del</button> 
                </li>`;
            });
        });
}

let currentIndicatorId = null;

function saveIndicator() {
    const title = document.getElementById("indicator-title").value;
    const code = document.getElementById("code").value;
    const OnGraph = document.getElementById("on_graph").checked;

    const url = currentIndicatorId
        ? `/customization/api/indicator/${currentIndicatorId}/` // Güncelleme için
        : "/customization/api/indicators/"; // Yeni ekleme için

    const method = currentIndicatorId ? 'PUT' : 'POST';
    //console.log(url,method)
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ title, code, on_graph: OnGraph })
    })
    
    .then(response => {
        if (!response.ok) throw new Error(response.statusText);
        return response.json();
    })
    .then(data => {
        showAlert(data.message, data.info);
        loadIndicators();
        //resetForm();
    })
    .catch(error => {
        alert(`An error occurred: ${error.message}`);
    });
}

function editIndicator(id) {
    fetch(`/customization/api/indicators/${id}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("indicator-title").value = data.title;           
            document.getElementById("code").value = data.code;
            document.getElementById("on_graph").checked = data.on_graph;
            currentIndicatorId = id; // Güncelleme için ID'yi ayarla

            updateActiveIndicator(id);
        });
}

function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
}

function showAlert(message, type = 'info') {
    console.log(message)
    const alertBox = document.getElementById('custom-alert');
    const alertMessage = document.getElementById('alert-message');

    alertMessage.textContent = message;

    alertBox.classList.add("visible"); // Türüne göre sınıf ekle (success, warning, info vb.)
    alertBox.classList.add(type); // Türüne göre sınıf ekle (success, warning, info vb.)

    // 5 saniye sonra otomatik kapat
    setTimeout(() => {
        alertBox.classList.remove('visible'); // Tüm sınıfları kaldır
    }, 2500);
}

function resetForm() {
    document.getElementById("indicator-title").value = "";           
    document.getElementById("code").value = "";
    document.getElementById("on_graph").checked = false;
    currentIndicatorId = null; // Form sıfırlanınca ID'yi temizle
}

function updateActiveIndicator(id) {
    const indicatorItems = document.querySelectorAll("#indicatorList li");

    // Remove the active class from all list items
    indicatorItems.forEach(item => item.classList.remove("active"));

    // Find the clicked indicator and add the active class
    const activeItem = document.querySelector(`#indicatorList li[data-id='${id}']`);
    if (activeItem) {
        activeItem.classList.add("active");
    }
}

function deleteIndicator(id, event) {
    event.stopPropagation(); // Liste tıklamasını engelle
    if (confirm("Are you sure you want to delete this indicator?")) {
        // Silme işlemi burada yapılacak
        console.log(`Indicator with ID ${id} will be deleted.`);
        fetch(`/customization/api/indicatordel/${id}/`,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({id})
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            showAlert(data.message, data.info);
            loadIndicators();
            //resetForm();
        })
        .catch(error => {
            alert(`An error occurred: ${error.message}`);
        });
    }
}