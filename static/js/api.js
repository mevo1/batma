// HTML öğelerine referans al
const connectBtn = document.getElementById("connectBtn");
const disconnectBtn = document.getElementById("disconnectBtn");
const connectedMessage = document.getElementById("connectedMessage");
const actionButtons = document.getElementById("actionButtons");

// "Bağla" butonuna tıklama olayı
connectBtn.addEventListener("click", () => {
    const apiAddress = document.getElementById("apiAddress").value.trim();
    if (apiAddress) {
        connectedMessage.classList.remove("hidden");
        actionButtons.classList.remove("hidden");
    } else {
        alert("Lütfen API adresinizi girin.");
    }
});

// "Bağlantıyı kes" butonuna tıklama olayı
disconnectBtn.addEventListener("click", () => {
    connectedMessage.classList.add("hidden");
    actionButtons.classList.add("hidden");
});
