document.addEventListener("DOMContentLoaded", function () {
  let dateInput = document.getElementById("appointment_date");

  fetch("/get_selected_date/")
    .then(response => response.json())
    .then(data => {
      if (data.selected_date) {
        dateInput.value = data.selected_date;
      }
    });

  dateInput.addEventListener("change", function () {
    let selectedDate = this.value;

    fetch("/save_selected_date/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token }}"
      },
      body: JSON.stringify({ selected_date: selectedDate })
    });
  });
});


