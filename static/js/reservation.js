document.addEventListener("DOMContentLoaded", () => {
    const steps = {
        guests: document.querySelector("#step-guests"),
        date: document.querySelector("#step-date"),
        time: document.querySelector("#step-time"),
        details: document.querySelector("#step-details"),
    };

    const makeReservationButton = document.querySelector("#make-reservation-btn");
    const guestButtons = document.querySelectorAll(".guest-btn");
    const dateInput = document.querySelector("#reservation-date");
    const timeSlotsContainer = document.querySelector("#time-slots");
    const nextToTimeButton = document.querySelector("#next-to-time");

    let selectedGuests = null;
    let selectedDate = null;
    let selectedTime = null;

    if (dateInput) {
        const today = new Date().toISOString().split("T")[0];
        dateInput.setAttribute("min", today); // Prevent selecting past dates
    }

    const loadTimeSlots = (date) => {
        const now = new Date();
        const currentTimeInMinutes = now.getHours() * 60 + now.getMinutes();
        const isToday = date === now.toISOString().split("T")[0];

        fetch(`/check-availability?date=${date}&guests=${selectedGuests}`)
            .then((response) => response.json())
            .then((data) => {
                timeSlotsContainer.innerHTML = ""; // Clear previous slots

                data.slots.forEach((slot) => {
                    const [hours, minutes] = slot.time.split(":").map(Number);
                    const slotTimeInMinutes = hours * 60 + minutes;

                    // Skip past slots if today
                    if (isToday && slotTimeInMinutes <= currentTimeInMinutes) {
                        return;
                    }

                    const button = document.createElement("button");
                    button.textContent = slot.available
                        ? `Book ${slot.time}`
                        : `${slot.time} (Not Available)`;
                    button.disabled = !slot.available;
                    button.classList.add("time-slot-btn");
                    button.dataset.time = slot.time;

                    if (slot.available) {
                        button.addEventListener("click", () => {
                            selectedTime = slot.time;
                            document.querySelector("#time-hidden").value = selectedTime;

                            steps.time.classList.add("hidden");
                            steps.details.classList.remove("hidden");
                        });
                    }

                    timeSlotsContainer.appendChild(button);
                });

                if (!timeSlotsContainer.innerHTML) {
                    timeSlotsContainer.innerHTML = `<p>No available time slots for the selected date.</p>`;
                }
            })
            .catch((error) => {
                console.error("Error loading time slots:", error);
                timeSlotsContainer.innerHTML = `<p>Could not load time slots. Please try again later.</p>`;
            });
    };

    if (nextToTimeButton) {
        nextToTimeButton.addEventListener("click", () => {
            if (!dateInput.value) {
                alert("Please select a date.");
                return;
            }
            selectedDate = dateInput.value;
            steps.date.classList.add("hidden");
            steps.time.classList.remove("hidden");
            loadTimeSlots(selectedDate);
        });
    }

    if (makeReservationButton) {
        makeReservationButton.addEventListener("click", (e) => {
            e.preventDefault();
            const isLoggedIn = document.body.dataset.loggedIn === "true";

            if (!isLoggedIn) {
                window.location.href = "/login?next=/make-reservation";
            } else {
                selectedGuests = null;
                selectedDate = null;
                selectedTime = null;

                document.querySelector("#guests-hidden").value = "";
                document.querySelector("#date-hidden").value = "";
                document.querySelector("#time-hidden").value = "";

                Object.values(steps).forEach((step) => step.classList.add("hidden"));
                steps.guests.classList.remove("hidden");
            }
        });
    }

    if (guestButtons.length > 0) {
        guestButtons.forEach((btn) => {
            btn.addEventListener("click", (e) => {
                selectedGuests = e.target.dataset.guests;
                document.querySelector("#guests-hidden").value = selectedGuests;

                steps.guests.classList.add("hidden");
                steps.date.classList.remove("hidden");
            });
        });
    }
});
