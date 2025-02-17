

document.getElementById('btn-uploadImg').addEventListener('click', function () {
    var input = document.getElementById('imageUpload');
    var csrfToken = document.getElementById('csrfToken-img').value;
    var file = input.files[0];
    if (!file) {
        alert('Bạn chưa chọn ảnh!');
        return;
    }
    var formData = new FormData();
    formData.append('image', file);

    fetch('/update_pet_image/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
                window.location.href = '/appointment_registration/';

            }
        })
        .catch(error => {
            console.error('Lỗi:', error);
        });
});