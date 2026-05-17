// =========================
// MEMBER 1 - LIVE SEARCH
// =========================
function searchEquipment() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let items = document.getElementsByClassName("equipment-item");

    for (let i = 0; i < items.length; i++) {
        let text = items[i].innerText.toLowerCase();
        items[i].style.display = text.includes(input) ? "" : "none";
    }
}


// =========================
// MEMBER 2 - CONFIRM ACTION
// =========================
function confirmAction(msg) {
    return confirm(msg);
}


// =========================
// MEMBER 3 - AUTO HIDE TOAST
// =========================
setTimeout(() => {
    let toasts = document.querySelectorAll("#toastContainer > div");

    toasts.forEach(toast => {
        toast.style.transition = "0.5s";
        toast.style.opacity = "0";

        setTimeout(() => toast.remove(), 500);
    });

}, 3000);