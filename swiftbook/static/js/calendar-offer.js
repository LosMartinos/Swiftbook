// calendar-offer.js
const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
    ];

const dayNames = [
    "Mo", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
]

document.addEventListener("DOMContentLoaded", () => {
    const calendarContainer = document.getElementById("calendar");
    const weekRange = document.getElementById("week-range");
    const prevWeekBtn = document.getElementById("prev-week");
    const nextWeekBtn = document.getElementById("next-week");
    const bookingContainer = document.getElementById("booking-container");

    let currentDate = new Date();
    let selectedTimeslot = null;
    let selectedDate = null;

    function formatDate(date) {
        return date.toISOString().split('T')[0];
    }

    function getWeekDates(date) {
        const start = new Date(date.setDate(date.getDate() - date.getDay()));
        const end = new Date(date.setDate(date.getDate() - date.getDay() + 6));
        return { start, end };
    }

    function updateWeekRange() {
        const { start, end } = getWeekDates(new Date(currentDate));
        if (start.getMonth() === end.getMonth()) {
            weekRange.textContent = `${monthNames[start.getMonth()]} ${start.getFullYear()}`;
        } else {
            weekRange.textContent = `${monthNames[start.getMonth()]} - ${monthNames[end.getMonth()]} ${end.getFullYear()}`;
        }
    }

    function loadTimeslots() {
        const { start, end } = getWeekDates(new Date(currentDate));
        fetch(`/api/timeslots?start=${formatDate(start)}&end=${formatDate(end)}`)
            .then(response => response.json())
            .then(data => {
                calendarContainer.innerHTML = '';
                for (let i = 0; i < 7; i++) {
                    const day = new Date(start);
                    day.setDate(start.getDate() + i);
                    const dayDiv = document.createElement('div');
                    dayDiv.className = 'calendar-day';
                    dayDiv.innerHTML = `<p>${dayNames[day.getDay()]}</p><h3>${day.getDate()}</h3><hr>`;
                    const timeslots = data[formatDate(day)] || [];
                    timeslots.forEach(timeslot => {
                        const slotDiv = document.createElement('div');
                        slotDiv.className = `timeslot ${timeslot.is_free ? 'free' : 'booked'}`;
                        slotDiv.textContent = timeslot.time;
                        if (timeslot.is_free) {
                            slotDiv.addEventListener('click', () => selectTimeslot(timeslot, formatDate(day)));
                        }
                        dayDiv.appendChild(slotDiv);
                    });
                    calendarContainer.appendChild(dayDiv);
                }
            });
    }

    function selectTimeslot(timeslot, date) {
        selectedTimeslot = timeslot;
        selectedDate = date;
        displaySelectedTimeslot();
    }

    function formatHumanReadableDate(isoDate) {
        const date = new Date(isoDate);
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Intl.DateTimeFormat('en-US', options).format(date);
    }

    function displaySelectedTimeslot() {
        if (!selectedTimeslot || !selectedDate) return;

        const humanReadableDate = formatHumanReadableDate(selectedDate);

        bookingContainer.innerHTML = `
            <div>
                <p>Selected Timeslot: ${humanReadableDate} at ${selectedTimeslot.time}</p>
                <button id="book-button">Book</button>
                <p id="booking-message"></p>
            </div>
        `;

        document.getElementById('book-button').addEventListener('click', () => {
            bookTimeslot(selectedTimeslot.id);
        });
    }

    function bookTimeslot(id) {
        const bookButton = document.getElementById('book-button');
        const bookingMessage = document.getElementById('booking-message');

        bookButton.classList.add('loading');
        bookButton.disabled = true;

        fetch(`/api/book`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id })
        })
        .then(response => response.json())
        .then(data => {
            bookButton.classList.remove('loading');
            bookButton.disabled = false;

            if (data.success) {
                bookingMessage.textContent = 'Booking successful!';
                bookButton.style.display = 'none';
                loadTimeslots();
            } else {
                bookingMessage.textContent = 'Something went wrong, try again later.';
            }
        })
        .catch(() => {
            bookButton.classList.remove('loading');
            bookButton.disabled = false;
            bookingMessage.textContent = 'Something went wrong, try again later.';
        });
    }

    prevWeekBtn.addEventListener('click', () => {
        currentDate.setDate(currentDate.getDate() - 7);
        updateWeekRange();
        loadTimeslots();
    });

    nextWeekBtn.addEventListener('click', () => {
        currentDate.setDate(currentDate.getDate() + 7);
        updateWeekRange();
        loadTimeslots();
    });

    updateWeekRange();
    loadTimeslots();
});
