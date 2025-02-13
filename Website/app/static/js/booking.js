function confirmBooking() {
    return confirm('Kiểm tra kĩ lại thông tin trước khi đặt lịch nha!')
}

document.getElementById("bookingForm").addEventListener("submit", function (event) {
    const checkboxes = document.querySelectorAll("input[type='checkbox']");
    let isChecked = false;

    checkboxes.forEach((checkbox) => {
        if (checkbox.checked) {
            isChecked = true;
        }
    });

    if (!isChecked) {
        event.preventDefault();
        alert("Vui lòng chọn ít nhất một phương pháp điều trị!");
    }
});