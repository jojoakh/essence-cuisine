document.addEventListener("DOMContentLoaded", () => {
    // Select DOM elements
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

    // Step 0: Reset and start the reservation flow
    const startReservationProcess = () => {
        // Reset previous selections
        selectedGuests = null;
        selectedDate = null;
        selectedTime = null;

        document.querySelector("#guests-hidden").value = "";
        document.querySelector("#date-hidden").value = "";
        document.querySelector("#time-hidden").value = "";

        // Show the guests step and hide others
        Object.values(steps).forEach((step) => step.classList.add("hidden"));
        steps.guests.classList.remove("hidden");
    };

    // Handle "Make a Reservation" button click
    if (makeReservationButton) {
        makeReservationButton.addEventListener("click", (e) => {
            e.preventDefault();

            // Check if the user is logged in
            const isLoggedIn = document.body.dataset.loggedIn === "true";
            if (!isLoggedIn) {
                // Redirect to the login page with a return URL to resume the reservation
                window.location.href = "/login?next=/make-reservation";
            } else {
                // Start the reservation process
                startReservationProcess();
            }
        });
    }

    // Step 1: Handle Guest Selection
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

    // Step 2: Handle Date Selection
    if (dateInput) {
        // Set the minimum selectable date to today
        const today = new Date().toISOString().split('T')[0]; // 'YYYY-MM-DD'
        dateInput.setAttribute("min", today); // Set the minimum date
        dateInput.value = ""; // Clear any pre-set value

        dateInput.addEventListener("change", () => {
            selectedDate = dateInput.value;
            document.querySelector("#date-hidden").value = selectedDate;
        });
    }

    nextToTimeButton.addEventListener("click", () => {
        if (!selectedDate) {
            alert("Please select a date.");
            return;
        }
        steps.date.classList.add("hidden");
        steps.time.classList.remove("hidden");
        loadTimeSlots(selectedDate);
    });

    // Step 3: Load Time Slots
    const loadTimeSlots = (date) => {
        fetch(`/check-availability?date=${date}&guests=${selectedGuests}`)
            .then((response) => response.json())
            .then((data) => {
                timeSlotsContainer.innerHTML = ""; // Clear previous slots
                data.slots.forEach((slot) => {
                    const button = document.createElement("button");
                    button.textContent = slot.available ? `Book ${slot.time}` : `${slot.time} (Not Available)`;
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
            })
            .catch((error) => {
                console.error("Error loading time slots:", error);
                timeSlotsContainer.innerHTML = `<p>Could not load time slots. Please try again later.</p>`;
            });
    };
});
