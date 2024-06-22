document.addEventListener("DOMContentLoaded", () => {
    const calendarContainer = document.getElementById("calendar");
    const weekRange = document.getElementById("week-range");
    const prevWeekBtn = document.getElementById("prev-week");
    const nextWeekBtn = document.getElementById("next-week");
    const timeslotInfo = document.getElementById("timeslot-info");
    const timeslotMessage = document.getElementById("timeslot-message");

    let currentDate = new Date();
    let selectedTimeslot = null;
    let selectedDate = null;

    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

    function formatDate(date) {
        return date.toISOString().split('T')[0];
    }

    function getWeekDates(date) {
        const start = new Date(date.setDate(date.getDate() - date.getDay() + 1));
        const end = new Date(date.setDate(date.getDate() - date.getDay() + 7));
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
        const startISO = formatDate(start);
        const endISO = formatDate(end);

        fetch(`/api/provider_timeslots?start_date=${startISO}&end_date=${endISO}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);  // Log the entire data object to inspect its structure
                const providerTimeslots = data.provider_booked_timeslots;
                calendarContainer.innerHTML = '';

                for (let i = 0; i < 7; i++) {
                    const day = new Date(start);
                    day.setDate(start.getDate() + i);
                    const dayOfWeek = day.getDay();
                    const dayDiv = document.createElement('div');
                    dayDiv.className = 'calendar-day';
                    dayDiv.innerHTML = `<p>${dayNames[dayOfWeek]}</p><h3>${day.getDate()}</h3><hr>`;

                    const dayTimeslots = providerTimeslots.filter(slot => slot.date === formatDate(day));

                    dayTimeslots.forEach(slot => {
                        const slotDiv = document.createElement('div');
                        slotDiv.className = 'timeslot';

                        const startTime = new Date(`${formatDate(day)}T${slot.time}`);
                        const timeString = startTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                        slotDiv.textContent = `${timeString} - ${slot.service__name}`;
                        slotDiv.addEventListener('click', () => selectTimeslot(timeString, formatDate(day), slot));
                        dayDiv.appendChild(slotDiv);
                    });

                    if (dayTimeslots.length === 0) {
                        const slotDiv = document.createElement('div');
                        slotDiv.textContent = 'No bookings';
                        slotDiv.classList.add('no-timeslots');
                        slotDiv.classList.add('text-center');
                        dayDiv.appendChild(slotDiv);
                    }

                    calendarContainer.appendChild(dayDiv);
                }
            })
            .catch(error => {
                console.error('Error fetching timeslots:', error);
                calendarContainer.innerHTML = '<p>Error loading timeslots. Please try again later.</p>';
            });
    }

    function selectTimeslot(timeslot, date, slot) {
        selectedTimeslot = timeslot;
        selectedDate = date;
        displaySelectedTimeslot(slot);
    }

    function displaySelectedTimeslot(slot) {
        if (!selectedTimeslot || !selectedDate) {
            timeslotMessage.textContent = "No event selected, to view an event select it in the calendar first.";
            return;
        }

        const formattedDate = formatHumanReadableDate(selectedDate);
        const formattedLength = formatDuration(slot.service__length);
        const bookedBy = slot.booked_by__name ? slot.booked_by__name : "Available";
        const providerName = slot.provider__name;

        timeslotMessage.innerHTML = `
            <p><strong>Provider:</strong> ${providerName}</p>
            <p><strong>Service:</strong> ${slot.service__name}</p>
            <p><strong>Date:</strong> ${formattedDate}</p>
            <p><strong>Time:</strong> ${selectedTimeslot}</p>
            <p><strong>Duration:</strong> ${formattedLength}</p>
            <p><strong>Booked by:</strong> ${bookedBy}</p>
        `;
    }

    function formatHumanReadableDate(isoDate) {
        const date = new Date(isoDate);
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Intl.DateTimeFormat('en-US', options).format(date);
    }

    function formatDuration(duration) {
        const parts = duration.split(':');
        const hours = parts[0] ? `${parts[0]} hours ` : '';
        const minutes = parts[1] ? `${parts[1]} minutes ` : '';
        const seconds = parts[2] ? `${parts[2]} seconds` : '';
        return `${hours}${minutes}${seconds}`.trim();
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
