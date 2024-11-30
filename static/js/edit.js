document.addEventListener("DOMContentLoaded", function () {
    // Fetch available time slots when the date changes
    document.getElementById("reservation-date").addEventListener("change", function () {
        const selectedDate = this.value; // Get the selected date
        const guestCount = document.querySelector("[name='guest_count']").value; // Get the number of guests

        // Ensure a date is selected
        if (!selectedDate) {
            alert("Please select a date.");
            return;
        }

        // Make a request to the server for available time slots
        fetch(`/check-availability/?date=${selectedDate}&guests=${guestCount}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch time slots.");
                }
                return response.json();
            })
            .then((data) => {
                const timeSlotsContainer = document.getElementById("time-slots");
                timeSlotsContainer.innerHTML = ""; // Clear previous time slots

                if (data.error) {
                    timeSlotsContainer.innerHTML = `<p class="text-danger">${data.error}</p>`;
                    return;
                }

                // Display the available time slots
                data.slots.forEach((slot) => {
                    if (slot.available) {
                        const button = document.createElement("button");
                        button.textContent = slot.time;
                        button.className = "btn btn-outline-primary m-1";
                        button.addEventListener("click", function () {
                            // Highlight the selected time slot and update the hidden input
                            document.querySelectorAll("#time-slots button").forEach((btn) => {
                                btn.classList.remove("btn-primary");
                                btn.classList.add("btn-outline-primary");
                            });
                            this.classList.remove("btn-outline-primary");
                            this.classList.add("btn-primary");
                            document.getElementById("reservation-time").value = slot.time; // Update hidden input
                        });
                        timeSlotsContainer.appendChild(button);
                    }
                });

                // If no slots are available
                if (!timeSlotsContainer.innerHTML) {
                    timeSlotsContainer.innerHTML = `<p class="text-danger">No available time slots for this date.</p>`;
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                document.getElementById("time-slots").innerHTML = `<p class="text-danger">An error occurred. Please try again later.</p>`;
            });
    });
});
