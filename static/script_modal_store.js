document.querySelectorAll('.iconstore').forEach(icon => {

    icon.addEventListener('click', (event) => {
        toggleModal(event);
    });
});

function toggleModal(event) {

    try {
        const srt_task = event.target.id;

        if (srt_task == 'today1') {
            const modalu = document.getElementById('taskModalToday');
            console.log(srt_task);
            modalu.style.display = modalu.style.display === "none" || modalu.style.display === "" ? "block" : "none";
            clearModalToday();
        }
    
        else if (srt_task == 'week2') {
            const modaln = document.getElementById('taskModalWeek');
            console.log(srt_task);
            modaln.style.display = modaln.style.display === "none" || modaln.style.display === "" ? "block" : "none";
            clearModalWeek();
        }
    
        else if (srt_task == 'month3') {
            const modalr = document.getElementById('taskModalMonth');
            console.log(srt_task);
            modalr.style.display = modalr.style.display === "none" || modalr.style.display === "" ? "block" : "none";
            clearModalMonth();
        }

    }
    catch {
        console.log('exit');
    }
}

// СЕГОДНЯ

function toggleReminderToday() {
    const reminderTimeContainer = document.getElementById('reminder-time-container-today');
    const reminderToggle = document.getElementById('reminder-toggle-today');
    reminderTimeContainer.style.display = reminderToggle.checked ? 'flex' : 'none';
}

async function addTaskToday(event) {
    const taskText = document.getElementById('task-text-today').value;
    const reminderEnabled = document.getElementById('reminder-toggle-today').checked;
    const reminderTime = reminderEnabled ? document.getElementById('reminder-time-today').value : null;
    const assignee = document.getElementById('assignee-today').value;
    const today = event.target.id;

    if (reminderTime === "") {
        reminderTime = 0;
    }

    //showNotificationToday(taskText, assignee);

    toggleModal(event);

    await updateContentToday(today.slice(0, -1), 'Сегодня', taskText, assignee, reminderEnabled ? `${reminderTime}` : 0);
}

function clearModalToday() {
    document.getElementById('task-text-today').value = '';

    document.getElementById('reminder-toggle-today').checked = false;

    document.getElementById('reminder-time-container-today').style.display = 'none';

    document.getElementById('reminder-time-today').value = '';
}

// НА НЕДЕЛЕ

function toggleReminderWeek() {
    const reminderTimeContainer = document.getElementById('reminder-time-container-week');
    const reminderToggle = document.getElementById('reminder-toggle-week');
    reminderTimeContainer.style.display = reminderToggle.checked ? 'flex' : 'none';
}

async function addTaskWeek(event) {
    const taskText = document.getElementById('task-text-week').value;
    const reminderEnabled = document.getElementById('reminder-toggle-week').checked;
    const reminderTime = reminderEnabled ? document.getElementById('reminder-time-week').value : null;
    const assignee = document.getElementById('assignee-week').value;
    const week = event.target.id;

    if (reminderTime === "") {
        reminderTime = 0;
    }

    //showNotificationWeek(taskText, assignee);

    toggleModal(event);

    await updateContentWeek(week.slice(0, -1), 'На неделе', taskText, assignee, reminderEnabled ? `${reminderTime}` : 0);
}

function clearModalWeek() {
    document.getElementById('task-text-week').value = '';

    document.getElementById('reminder-toggle-week').checked = false;

    document.getElementById('reminder-time-container-week').style.display = 'none';

    document.getElementById('reminder-time-week').value = '';
}

// В ТЕЧЕНИЕ МЕСЯЦА

function toggleReminderMonth() {
    const reminderTimeContainer = document.getElementById('reminder-time-container-month');
    const reminderToggle = document.getElementById('reminder-toggle-month');
    reminderTimeContainer.style.display = reminderToggle.checked ? 'flex' : 'none';
}

async function addTaskMonth(event) {
    const taskText = document.getElementById('task-text-month').value;
    const reminderEnabled = document.getElementById('reminder-toggle-month').checked;
    const reminderTime = reminderEnabled ? document.getElementById('reminder-time-month').value : null;
    const assignee = document.getElementById('assignee-month').value;
    const month = event.target.id;

    if (reminderTime === "") {
        reminderTime = 0;
    }

    //showNotificationMonth(taskText, assignee);

    toggleModal(event);

    await updateContentMonth(month.slice(0, -1), 'В течении месяца', taskText, assignee, reminderEnabled ? `${reminderTime}` : 0);
}

function clearModalMonth() {
    document.getElementById('task-text-month').value = '';

    document.getElementById('reminder-toggle-month').checked = false;

    document.getElementById('reminder-time-container-month').style.display = 'none';

    document.getElementById('reminder-time-month').value = '';
}

function showNotificationMonth(taskText, assignee) {
    if (Notification.permission === "granted") {
        const notification = new Notification(`${taskText}`, {
            body: `Дело: В течении месяца\nНазначено: ${assignee}`
        });

        notification.onclick = () => {
            window.location.href = "/store";
        };
    }
}

function showNotificationWeek(taskText, assignee) {
    if (Notification.permission === "granted") {
        const notification = new Notification(`${taskText}`, {
            body: `Дело: На неделе\nНазначено: ${assignee}`
        });

        notification.onclick = () => {
            window.location.href = "/store";
        };
    }
}

function showNotificationToday(taskText, assignee) {
    if (Notification.permission === "granted") {
        const notification = new Notification(`${taskText}`, {
            body: `Дело: Сегодня\nНазначено: ${assignee}`
        });

        notification.onclick = () => {
            window.location.href = "/store";
        };
    }
}


async function updateContentToday(case_id, case_text, text_task, user_name, reminder) {
    const contentData = {
        case_id: case_id,
        case_text: case_text,
        text_task: text_task,
        user_name: user_name,
        reminder: reminder,
    };

    const response = await fetch("/today", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(contentData)
    });

    const result = await response.json();

    if (response.ok){
        window.location.href = result.data;
    }
}

async function updateContentWeek(case_id, case_text, text_task, user_name, reminder) {
    const contentData = {
        case_id: case_id,
        case_text: case_text,
        text_task: text_task,
        user_name: user_name,
        reminder: reminder,
    };

    const response = await fetch("/week", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(contentData)
    });

    const result = await response.json();

    if (response.ok){
        window.location.href = result.data;
    }
}

async function updateContentMonth(case_id, case_text, text_task, user_name, reminder) {
    const contentData = {
        case_id: case_id,
        case_text: case_text,
        text_task: text_task,
        user_name: user_name,
        reminder: reminder,
    };

    const response = await fetch("/month", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(contentData)
    });

    const result = await response.json();

    if (response.ok){
        window.location.href = result.data;
    }
}
