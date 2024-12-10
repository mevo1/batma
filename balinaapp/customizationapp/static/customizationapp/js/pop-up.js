document.addEventListener('DOMContentLoaded', () => {
    const popups = document.querySelectorAll('.popup');
    popups.forEach(popup => {
        setTimeout(() => {
            popup.style.display = 'none';
        }, 5000); // 3 saniye sonra kaybolacak
    });
});
