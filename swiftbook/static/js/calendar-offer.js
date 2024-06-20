document.addEventListener("DOMContentLoaded", () => {
    const calendarContainer = document.getElementById("calendar");
    const weekRange = document.getElementById("week-range");
    const prevWeekBtn = document.getElementById("prev-week");
    const nextWeekBtn = document.getElementById("next-week");
    const timeslotInfo = document.getElementById("timeslot-info");
    const timeslotMessage = document.getElementById("timeslot-message");
    const weatherContainer = document.getElementById("weather-container");
    const mapImage = document.getElementById("mapImage")

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
    
        fetch(`/api/timeslots?start=${formatDate(start)}&end=${formatDate(end)}&provider_id=${serviceData.providerId}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);  // Log the entire data object to inspect its structure
                const { timeslots, business_hours } = data;
                calendarContainer.innerHTML = '';
    
                for (let i = 0; i < 7; i++) {
                    const day = new Date(start);
                    day.setDate(start.getDate() + i);
                    const dayOfWeek = day.getDay();
                    const dayDiv = document.createElement('div');
                    dayDiv.className = 'calendar-day';
                    dayDiv.innerHTML = `<p>${dayNames[dayOfWeek]}</p><h3>${day.getDate()}</h3><hr>`;
    
                    if (business_hours[dayOfWeek]) {
                        const { open_time, close_time } = business_hours[dayOfWeek];
    
                        // Convert service length from "HH:MM:SS" to minutes
                        const serviceLength = parseDurationToMinutes(serviceData.serviceDuration);
    
                        let currentTime = new Date(`${formatDate(day)}T${open_time}`);
                        const endTime = new Date(`${formatDate(day)}T${close_time}`);
    
                        while (currentTime <= endTime) {
                            const slotDiv = document.createElement('div');
                            slotDiv.className = 'timeslot';
    
                            const timeString = currentTime.toTimeString().substr(0, 5);
                            const endTimeString = new Date(currentTime.getTime() + serviceLength * 60000).toTimeString().substr(0, 5);
    
                            if (timeslots[formatDate(day)]) {
                                const isBooked = timeslots[formatDate(day)].some(slot => slot.time === timeString);
                                slotDiv.textContent = `${timeString} - ${endTimeString}`;
                                slotDiv.classList.add(isBooked ? 'booked' : 'free');
                                if (!isBooked) {
                                    slotDiv.addEventListener('click', () => selectTimeslot(timeString, formatDate(day)));
                                }
                            } else {
                                slotDiv.textContent = `${timeString} - ${endTimeString}`;
                                slotDiv.classList.add('free');
                                slotDiv.addEventListener('click', () => selectTimeslot(timeString, formatDate(day)));
                            }
    
                            dayDiv.appendChild(slotDiv);
    
                            currentTime.setMinutes(currentTime.getMinutes() + serviceLength);
                        }
                    } else {
                        const slotDiv = document.createElement('div');
                        slotDiv.textContent = 'Closed';
                        slotDiv.classList.add('closed');
                        dayDiv.appendChild(slotDiv);
                    }
    
                    calendarContainer.appendChild(dayDiv);
                }
            });
    }
    
    function parseDurationToMinutes(durationString) {
        const [hours, minutes, seconds] = durationString.split(':').map(Number);
        return hours * 60 + minutes;
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
        if (!selectedTimeslot || !selectedDate) {
            timeslotMessage.textContent = "No timeslot selected, to make a booking select a timeslot in the calendar first.";
            return;
        }
    
        const formattedDate = formatHumanReadableDate(selectedDate);
        timeslotMessage.innerHTML = `You have selected:<br><strong>${formattedDate}</strong> at <strong>${selectedTimeslot}</strong>`;
        // Fetch and display weather data for the selected date
        fetchWeather(selectedDate);
}

function fetchWeather(date) {
    const latitude = '{{ service.provider.latitude }}';
    const longitude = '{{ service.provider.longitude }}';
    const apiKey = 'your-openweathermap-api-key';  // Replace with your OpenWeatherMap API key
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const temperature = (data.main.temp - 273.15).toFixed(2); // Convert from Kelvin to Celsius
            const description = data.weather[0].description;
            const iconUrl = `http://openweathermap.org/img/wn/${data.weather[0].icon}.png`;

            weatherContainer.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Weather on Selected Date</h5>
                        <img src="${iconUrl}" alt="${description}" />
                        <p>Temperature: ${temperature}°C</p>
                        <p>Description: ${description}</p>
                    </div>
                </div>
            `;
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            weatherContainer.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Weather on Selected Date</h5>
                        <p>Could not fetch weather data.</p>
                    </div>
                </div>
            `;
        });
}

function bookAppointment() {
    if (!selectedTimeslot || !selectedDate) return;

    fetch('/api/book/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': serviceData.csrfToken,
        },
        body: JSON.stringify({
            provider_id: serviceData.providerId,
            service_id: serviceData.serviceId,
            date: selectedDate,
            time: selectedTimeslot,
        }),
    })
        .then(response => {
            if (response.ok) {
                alert('Appointment booked successfully!');
            } else {
                alert('Failed to book appointment.');
            }
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
})