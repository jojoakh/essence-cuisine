document.addEventListener("DOMContentLoaded", () => {
    // Handle dismissible Bootstrap alerts
    const alertCloseButtons = document.querySelectorAll(".btn-close");
    alertCloseButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            btn.closest(".alert").classList.add("d-none");
        });
    });

    // Smooth scrolling for anchor links (if added in navigation or other sections)
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach((link) => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const targetId = link.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: "smooth" });
            }
        });
    });
});
