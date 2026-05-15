function applyTheme(theme) {
    if (theme === "dark") {
        document.documentElement.classList.add("dark");
    } else {
        document.documentElement.classList.remove("dark");
    }
}

function toggleTheme() {
    let current = localStorage.getItem("theme");

    if (current === "dark") {
        localStorage.setItem("theme", "light");
        applyTheme("light");
    } else {
        localStorage.setItem("theme", "dark");
        applyTheme("dark");
    }
}

/* INIT THEME ON LOAD */
window.addEventListener("load", function () {
    let saved = localStorage.getItem("theme") || "light";
    applyTheme(saved);
});