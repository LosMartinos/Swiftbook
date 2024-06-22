document.addEventListener("DOMContentLoaded", () => {
    const calendarContainer = document.getElementById("calendar");
    const weekRange = document.getElementById("week-range");
    const prevWeekBtn = document.getElementById("prev-week");
    const nextWeekBtn = document.getElementById("next-week");
    const timeslotInfo = document.getElementById("timeslot-info");
    const timeslotMessage = document.getElementById("timeslot-message");
    const weatherContainer = document.getElementById("weather-container");

    
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
        
        /*
        fetch(`/api/user_timeslots?start_date=${startISO}&end_date=${endISO}`, {
            headers: {
                'Accept': 'application/xml'  // Request XML response
            }
        })
        .then(response => response.text())  // Get response as text
        .then(str => new window.DOMParser().parseFromString(str, "text/xml"))  // Parse the text to XML
        .then(data => {
            console.log(data);  // Log the parsed XML document object
        */
    
        // Fetch timeslots for the current user within the specified range
        fetch(`/api/user_timeslots?start_date=${startISO}&end_date=${endISO}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);  // Log the entire data object to inspect its structure
                const userTimeslots = data.user_booked_timeslots;
                calendarContainer.innerHTML = '';

                for (let i = 0; i < 7; i++) {
                    const day = new Date(start);
                    day.setDate(start.getDate() + i);
                    const dayOfWeek = day.getDay();
                    const dayDiv = document.createElement('div');
                    dayDiv.className = 'calendar-day';
                    dayDiv.innerHTML = `<p>${dayNames[dayOfWeek]}</p><h3>${day.getDate()}</h3><hr>`;

                    // Filter user timeslots for the current day
                    const dayTimeslots = userTimeslots.filter(slot => slot.date === formatDate(day));

                    dayTimeslots.forEach(slot => {
                        const slotDiv = document.createElement('div');
                        slotDiv.className = 'timeslot';

                        const startTime = new Date(`${formatDate(day)}T${slot.time}`);
                        const timeString = startTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                        

                        slotDiv.textContent = `${timeString} at ${slot.service__provider__name}`;
                        slotDiv.addEventListener('click', () => selectTimeslot(timeString, formatDate(day), slot));
                        dayDiv.appendChild(slotDiv);
                    });

                    if (dayTimeslots.length === 0) {
                        const slotDiv = document.createElement('div');
                        slotDiv.textContent = 'No events planned';
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
        timeslotMessage.innerHTML = `You have selected:<br><strong>${slot.service__provider__name}</strong> - <strong>
                                    ${slot.service__name}</strong><br><strong>${formattedDate}</strong> at <strong>${selectedTimeslot}</strong>
                                    <br>Duration: ${slot.service__length}`;
    
    }

    function formatHumanReadableDate(isoDate) {
        const date = new Date(isoDate);
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Intl.DateTimeFormat('en-US', options).format(date);
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
