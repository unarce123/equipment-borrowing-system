
// LIVE SEARCH - UNARCE

function searchEquipment() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let items = document.getElementsByClassName("equipment-item");

    for (let i = 0; i < items.length; i++) {
        let text = items[i].innerText.toLowerCase();
        items[i].style.display = text.includes(input) ? "" : "none";
    }
}



// CONFIRM SYSTEM - UTINAS


document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll("a[data-confirm]").forEach(link => {

        link.addEventListener("click", function (e) {

            const message = this.getAttribute("data-confirm") || "Are you sure?";

            if (!confirm(message)) {
                e.preventDefault();
            }

        });

    });

});



// AUTO HIDE TOAST - VILLAREAL

setTimeout(() => {
    let toasts = document.querySelectorAll("#toastContainer > div");

    toasts.forEach(toast => {
        toast.style.transition = "0.5s";
        toast.style.opacity = "0";

        setTimeout(() => toast.remove(), 500);
    });

}, 3000);