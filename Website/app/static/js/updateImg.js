const modal_img = document.getElementById("editModal-updateImg");
const btn_img = document.getElementById("editBtn-updateImg");
const closeBtn_img = document.querySelector(".close-updateImg");

btn_img.onclick = function () {
    modal_img.style.display = "flex";
}

closeBtn_img.onclick = function () {
    modal_img.style.display = "none";
}


const btnCustomer = document.querySelector(".btn-save-Customer");



btn_updateImg = btnCustomer;
url = "/update_customer_image/";





document.addEventListener("click", function (event) {
    if (btn_updateImg && event.target === btn_updateImg) {
        console.log("Nút cập nhật ảnh được nhấn:", btn_updateImg);
        console.log(url);

        const fileInput = document.getElementById("imageUpload");
        const csrfToken = document.getElementById("csrfToken-img").value;

        if (!fileInput.files || fileInput.files.length === 0) {
            alert("Vui lòng chọn ảnh trước khi tải lên!");
            return;
        }

        const formData = new FormData();
        formData.append("image", fileInput.files[0]);

        fetch(url, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": csrfToken
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Tải ảnh lên thành công!");
                    modal_img.style.display = "none";
                    location.reload();
                } else {
                    alert("Tải ảnh lên thất bại!");
                }
            })
            .catch(error => {
                console.error("Lỗi:", error);
                alert("Không thể kết nối đến máy chủ.");
            });
    }
});