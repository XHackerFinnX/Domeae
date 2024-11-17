document.querySelectorAll('.iconstudy').forEach(icon => {

    icon.addEventListener('click', (event) => {
        toggleModal(event);
    });
});

function toggleModal(event) {

    try {
        const srt_task = event.target.id;

        if (srt_task == 'homework1') {
            const modalu = document.getElementById('taskModalHomework');
            console.log(srt_task);
            modalu.style.display = modalu.style.display === "none" || modalu.style.display === "" ? "block" : "none";
            clearModalHomework();
        }
    
        else if (srt_task == 'exam2') {
            const modaln = document.getElementById('taskModalExam');
            console.log(srt_task);
            modaln.style.display = modaln.style.display === "none" || modaln.style.display === "" ? "block" : "none";
            clearModalExam();
        }

    }
    catch {
        console.log('exit');
    }
}

// ДОМАШНИЕ ЗАДАНИЯ

function toggleReminderHomework() {
    const reminderTimeContainer = document.getElementById('reminder-time-container-homework');
    const reminderToggle = document.getElementById('reminder-toggle-homework');
    reminderTimeContainer.style.display = reminderToggle.checked ? 'flex' : 'none';
}

async function addTaskHomework(event) {
    const taskText = document.getElementById('task-text-homework').value;
    const reminderEnabled = document.getElementById('reminder-toggle-homework').checked;
    const reminderTime = reminderEnabled ? document.getElementById('reminder-time-homework').value : null;
    const today = event.target.id;

    if (reminderTime === "") {
        reminderTime = 0;
    }

    toggleModal(event);

    await updateContentHomework(today.slice(0, -1), 'Домашние задания', taskText, reminderEnabled ? `${reminderTime}` : 0);
}

function clearModalHomework() {
    document.getElementById('task-text-homework').value = '';

    document.getElementById('reminder-toggle-homework').checked = false;

    document.getElementById('reminder-time-container-homework').style.display = 'none';

    document.getElementById('reminder-time-homework').value = '';
}

// ЭКЗАМЕНЫ

function toggleReminderExam() {
    const reminderTimeContainer = document.getElementById('reminder-time-container-exam');
    const reminderToggle = document.getElementById('reminder-toggle-exam');
    reminderTimeContainer.style.display = reminderToggle.checked ? 'flex' : 'none';
}

async function addTaskExam(event) {
    const taskText = document.getElementById('task-text-exam').value;
    const reminderEnabled = document.getElementById('reminder-toggle-exam').checked;
    const reminderTime = reminderEnabled ? document.getElementById('reminder-time-exam').value : null;
    const week = event.target.id;

    if (reminderTime === "") {
        reminderTime = 0;
    }

    toggleModal(event);

    await updateContentExam(week.slice(0, -1), 'Экзамены', taskText, reminderEnabled ? `${reminderTime}` : 0);
}

function clearModalExam() {
    document.getElementById('task-text-exam').value = '';

    document.getElementById('reminder-toggle-exam').checked = false;

    document.getElementById('reminder-time-container-exam').style.display = 'none';

    document.getElementById('reminder-time-exam').value = '';
}


async function updateContentHomework(case_id, case_text, text_task, reminder) {
    const contentData = {
        case_id: case_id,
        case_text: case_text,
        text_task: text_task,
        reminder: reminder,
    };

    const response = await fetch("/homework", {
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

async function updateContentExam(case_id, case_text, text_task, reminder) {
    const contentData = {
        case_id: case_id,
        case_text: case_text,
        text_task: text_task,
        reminder: reminder,
    };

    const response = await fetch("/exam", {
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