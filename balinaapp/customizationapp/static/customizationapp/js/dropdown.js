
function setSelection(buttonId, inputId, value, readableValue) {
    
    // Gizli input alanına değeri ayarla
    document.getElementById(inputId).value = value;
    //console.log(document.getElementById('dropdown1').value)
    // Dropdown butonunun üzerindeki metni güncelle
    document.getElementById(buttonId).innerText = readableValue;
}