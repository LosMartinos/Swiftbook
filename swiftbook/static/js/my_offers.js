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
        const formattedLength = slot.service__length; // Use the already formatted length from the response
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

    window.editDescription = function(serviceId) {
        const descriptionElement = document.getElementById(`service-description-${serviceId}`);
        const textareaElement = document.getElementById(`edit-description-${serviceId}`);
        const saveButton = document.getElementById(`save-description-btn-${serviceId}`);
        
        descriptionElement.classList.add('d-none');
        textareaElement.classList.remove('d-none');
        saveButton.classList.remove('d-none');
    }

    window.saveDescription = function(serviceId) {
        const textareaElement = document.getElementById(`edit-description-${serviceId}`);
        const newDescription = textareaElement.value;

        fetch('/update_service_description', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ id: serviceId, description: newDescription })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const descriptionElement = document.getElementById(`service-description-${serviceId}`);
                descriptionElement.textContent = newDescription;

                descriptionElement.classList.remove('d-none');
                textareaElement.classList.add('d-none');
                document.getElementById(`save-description-btn-${serviceId}`).classList.add('d-none');
            } else {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error updating description:', error);
            alert('An error occurred while updating the description. Please try again.');
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    updateWeekRange();
    loadTimeslots();
});
