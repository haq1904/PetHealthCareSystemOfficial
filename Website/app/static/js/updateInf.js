const modal = document.getElementById("editModal");
const btn = document.getElementById("editBtn");
const closeBtn = document.querySelector(".close");

btn.onclick = function () {
    modal.style.display = "flex"; // Hiển thị modal khi nhấn nút
}

closeBtn.onclick = function () {
    modal.style.display = "none"; // Ẩn modal khi nhấn nút đóng
}

window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = "none"; // Ẩn modal nếu click ra ngoài vùng modal
    }
}