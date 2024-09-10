document.addEventListener("DOMContentLoaded", function() {
    // Select all tab buttons and content sections
    const tabs = document.querySelectorAll(".meal-planner-tabs .tab");
    const contents = document.querySelectorAll(".tab-content");

    // Function to handle tab switching
    function switchTab(event) {
        // Remove active class from all tabs and hide all contents
        tabs.forEach(tab => tab.classList.remove("active"));
        contents.forEach(content => content.style.display = "none");

        // Add active class to clicked tab
        event.currentTarget.classList.add("active");

        // Show the corresponding content
        const index = Array.from(tabs).indexOf(event.currentTarget);
        contents[index].style.display = "block";
    }

    // Attach click event to each tab button
    tabs.forEach((tab, index) => {
        tab.addEventListener("click", switchTab);
    });

    // Show the first tab content by default
    if (contents.length > 0) {
        contents[0].style.display = "block";
    }
});

document.addEventListener("DOMContentLoaded", function () {
    // Initialize FullCalendar
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: [
            // Example events data
            {
                title: 'Breakfast',
                start: '2024-09-10T09:00:00',
                end: '2024-09-10T10:00:00',
            },
            {
                title: 'Lunch',
                start: '2024-09-11T12:00:00',
            }
        ]
    });
    calendar.render();

    // Tab switching logic
    const tabs = document.querySelectorAll(".meal-planner-tabs .tab");
    const contents = document.querySelectorAll(".tab-content");

    function switchTab(event) {
        tabs.forEach(tab => tab.classList.remove("active"));
        contents.forEach(content => content.style.display = "none");

        event.currentTarget.classList.add("active");
        const index = Array.from(tabs).indexOf(event.currentTarget);
        contents[index].style.display = "block";
    }

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", switchTab);
    });

    // Show the first tab content by default
    if (contents.length > 0) {
        contents[0].style.display = "block";
    }
});
9