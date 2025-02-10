


const modal = document.getElementById("editModal-updateInf");
const btn = document.getElementById("editBtn-updateInf");
const closeBtn = document.querySelector(".close-updateInf");

const saveButton = document.getElementById("saveBtn-updateInf");
const addressInput = document.getElementById("address");
const phoneInput = document.getElementById("phone");


btn.onclick = function () {
    modal.style.display = "flex";
};

closeBtn.onclick = function () {
    modal.style.display = "none";
};








saveButton.addEventListener("click", function () {
    if (addressInput.value.trim() === "") {
        addressInput.setCustomValidity("Vui lòng nhập địa chỉ!");
        addressInput.reportValidity();
        return;
    } else {
        addressInput.setCustomValidity("");
    }

    if (phoneInput.value.trim() === "") {
        phoneInput.setCustomValidity("Vui lòng nhập số điện thoại!");
        phoneInput.reportValidity();
        return;
    } else {
        phoneInput.setCustomValidity("");
    }


    const addressValue = addressInput.value.trim();
    const phoneValue = phoneInput.value.trim();
    const csrfToken = document.getElementById('csrfToken-inf').value;

    const updatedData = {
        address: addressValue,
        phone: phoneValue,
    };

    const url = "/update_customer_info/";

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(updatedData),
    })
        .then((response) => {
            if (response.ok) {
                alert("Cập nhật thông tin thành công!");
                // Đóng modal sau khi cập nhật thành công
                modal.style.display = "none";
                location.reload();
            } else {
                alert("Có lỗi xảy ra khi cập nhật thông tin.");
            }
        })
        .catch((error) => {
            console.error("Lỗi:", error);
            alert("Không thể kết nối đến máy chủ.");
        });
});


