let currentApiId = null;

function saveApi() {
    const name = document.getElementById("apiName").value;
    const adress = document.getElementById("apiAddress").value;
    const secretkey = document.getElementById("apiSecret").value;

    const url = currentApiId
        ? `/connection/api/api/${currentApiId}/` // Güncelleme için
        : "/connection/api/apis/"; // Yeni ekleme için

    const method = currentApiId ? 'PUT' : 'POST';
    //console.log(url,method)
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ name, adress, secretkey })
    })
    
    .then(response => {
        if (!response.ok) throw new Error(response.statusText);
        return response.json();
    })
    .then(data => {
        //alert('Saved successfully.')
        showAlert(data.message, data.info);
        //loadIndicators();
        //resetForm();
    })
    .catch(error => {
        alert(`An error occurred: ${error.message}`);
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
    }, 10000);
}