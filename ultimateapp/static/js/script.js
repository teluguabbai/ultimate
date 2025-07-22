document.addEventListener("DOMContentLoaded", () => {
    // Sticky header effect
    window.addEventListener("scroll", () => {
        const header = document.querySelector("header");
        if (window.scrollY > 50) {
            header.style.background = "rgba(0, 0, 0, 0.95)";
        } else {
            header.style.background = "rgba(0, 0, 0, 0.8)";
        }
    });

    // Smooth scrolling
    document.querySelectorAll("nav a").forEach(anchor => {
        anchor.addEventListener("click", (event) => {
            event.preventDefault();
            document.querySelector(anchor.getAttribute("href")).scrollIntoView({ behavior: "smooth" });
        });
    });
});
