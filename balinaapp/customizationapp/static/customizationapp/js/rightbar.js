document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar-right");
    const toggleBtn = document.getElementById("toggleSidebar-right");

    toggleBtn.addEventListener("click", function () {
        sidebar.classList.toggle("open");
    });
});