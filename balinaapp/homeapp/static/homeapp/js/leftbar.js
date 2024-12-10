document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar-left");
    const toggleBtn = document.getElementById("toggleSidebar-left");

    toggleBtn.addEventListener("click", function () {
        sidebar.classList.toggle("open");
    });
});
