document.querySelectorAll('.iconhome').forEach(icon => {

    icon.addEventListener('click', (event) => {
        toggleModal(event);
    });
});

function toggleModal(event) {

    try {
        const srt_task = event.target.id;

        if (srt_task == 'urgent1') {
            const modalu = document.getElementById('taskModalUrgent');
            console.log(srt_task);
            modalu.style.display = modalu.style.display === "none" || modalu.style.display === "" ? "block" : "none";
            clearModalUrgent();
        }
    
        else if (srt_task == 'normal2') {
            const modaln = document.getElementById('taskModalNormal');
            console.log(srt_task);
            modaln.style.display = modaln.style.display === "none" || modaln.style.display === "" ? "block" : "none";
            clearModalNormal();
        }
    
        else if (srt_task == 'regular3') {
            const modalr = document.getElementById('taskModalRegular');
            console.log(srt_task);
            modalr.style.display = modalr.style.display === "none" || modalr.style.display === "" ? "block" : "none";
            clearModalRegular();
        }

    }
    catch {
        console.log('exit');
    }
}

// СРОЧНЫЕ ДЕЛА

function toggleReminderUrgent() {
    const reminderTimeContainer = document.getElementById('reminder-time-container-urgent');
    const reminderToggle = document.getElementById('reminder-toggle-urgent');
    reminderTimeContainer.style.display = reminderToggle.checked ? 'flex' : 'none';
}

async function addTaskUrgent(event) {
    const taskText = document.getElementById('task-text-urgent').value;
    const reminderEnabled = document.getElementById('reminder-toggle-urgent').checked;
    const reminderTime = reminderEnabled ? document.getElementById('reminder-time-urgent').value : null;
    const assignee = document.getElementById('assignee-urgent').value;
    const urgent = event.target.id

    if (reminderTime === "") {
        reminderTime = 0;
    }

    showNotificationUrgent(taskText, assignee);

    toggleModal(event);
    
    await updateContentUrgent(urgent.slice(0, -1), 'Срочное дело', taskText, assignee, reminderEnabled ? `${reminderTime}` : 0);
}

function clearModalUrgent() {
    document.getElementById('task-text-urgent').value = '';

    document.getElementById('reminder-toggle-urgent').checked = false;

    document.getElementById('reminder-time-container-urgent').style.display = 'none';

    document.getElementById('reminder-time-urgent').value = '';
}

// ОБЫЧНЫЕ ДЕЛА

function toggleReminderNormal() {
    const reminderTimeContainer = document.getElementById('reminder-time-container-normal');
    const reminderToggle = document.getElementById('reminder-toggle-normal');
    reminderTimeContainer.style.display = reminderToggle.checked ? 'flex' : 'none';
}

async function addTaskNormal(event) {
    const taskText = document.getElementById('task-text-normal').value;
    const reminderEnabled = document.getElementById('reminder-toggle-normal').checked;
    const reminderTime = reminderEnabled ? document.getElementById('reminder-time-normal').value : null;
    const assignee = document.getElementById('assignee-normal').value;
    const urgent = event.target.id

    if (reminderTime === "") {
        reminderTime = 0;
    }

    //showNotificationNormal(taskText, assignee);

    toggleModal(event);

    await updateContentNormal(urgent.slice(0, -1), 'Обычное дело', taskText, assignee, reminderEnabled ? `${reminderTime}` : 0);

}

function clearModalNormal() {
    document.getElementById('task-text-normal').value = '';

    document.getElementById('reminder-toggle-normal').checked = false;

    document.getElementById('reminder-time-container-normal').style.display = 'none';

    document.getElementById('reminder-time-normal').value = '';
}

// РЕГУЛЯРНЫЕ ДЕЛА

function toggleReminderRegular() {
    const reminderTimeContainer = document.getElementById('reminder-time-container-regular');
    const reminderToggle = document.getElementById('reminder-toggle-regular');
    reminderTimeContainer.style.display = reminderToggle.checked ? 'flex' : 'none';
}

async function addTaskRegular(event) {
    const taskText = document.getElementById('task-text-regular').value;
    const reminderEnabled = document.getElementById('reminder-toggle-regular').checked;
    const reminderTime = reminderEnabled ? document.getElementById('reminder-time-regular').value : null;
    const assignee = document.getElementById('assignee-regular').value;
    const urgent = event.target.id

    if (reminderTime === "") {
        reminderTime = 0;
    }

    //showNotificationRegular(taskText, assignee);

    toggleModal(event);

    await updateContentRegular(urgent.slice(0, -1), 'Регулярное дело', taskText, assignee, reminderEnabled ? `${reminderTime}` : 0);

}

function clearModalRegular() {
    document.getElementById('task-text-regular').value = '';

    document.getElementById('reminder-toggle-regular').checked = false;

    document.getElementById('reminder-time-container-regular').style.display = 'none';

    document.getElementById('reminder-time-regular').value = '';
}

function showNotificationRegular(taskText, assignee) {
    if (Notification.permission === "granted") {
        const notification = new Notification(`${taskText}`, {
            body: `Дело: Регулярное\nНазначено: ${assignee}`
        });

        notification.onclick = () => {
            window.location.href = "/home";
        };
    }
}

function showNotificationNormal(taskText, assignee) {
    if (Notification.permission === "granted") {
        const notification = new Notification(`${taskText}`, {
            body: `Дело: Обычное\nНазначено: ${assignee}`
        });

        notification.onclick = () => {
            window.location.href = "/home";
        };
    }
}

function showNotificationUrgent(taskText, assignee) {
    if (Notification.permission === "granted") {
        const notification = new Notification(`${taskText}`, {
            body: `Дело: Срочное\nНазначено: ${assignee}`
        });

        notification.onclick = () => {
            window.location.href = "/home";
        };
    }
}

async function updateContentUrgent(case_id, case_text, text_task, user_name, reminder) {
    const contentData = {
        case_id: case_id,
        case_text: case_text,
        text_task: text_task,
        user_name: user_name,
        reminder: reminder,
    };

    const response = await fetch("/urgent", {
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

async function updateContentNormal(case_id, case_text, text_task, user_name, reminder) {
    const contentData = {
        case_id: case_id,
        case_text: case_text,
        text_task: text_task,
        user_name: user_name,
        reminder: reminder,
    };

    const response = await fetch("/normal", {
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

async function updateContentRegular(case_id, case_text, text_task, user_name, reminder) {
    const contentData = {
        case_id: case_id,
        case_text: case_text,
        text_task: text_task,
        user_name: user_name,
        reminder: reminder,
    };

    const response = await fetch("/regular", {
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
