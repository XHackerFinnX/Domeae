document.querySelectorAll('.iconplan').forEach(icon => {

    icon.addEventListener('click', (event) => {
        toggleModal(event);
    });
});

function toggleModal(event) {

    try {
        const srt_task = event.target.id;

        if (srt_task == 'plan1') {
            const modalu = document.getElementById('taskModalPlan');
            console.log(srt_task);
            modalu.style.display = modalu.style.display === "none" || modalu.style.display === "" ? "block" : "none";
            clearModalPlan();
        }

    }
    catch {
        console.log('exit');
    }
}

// В ПЛАНАХ

async function addTaskPlan(event) {
    const taskText = document.getElementById('task-text-plan').value;
    const today = event.target.id;

    toggleModal(event);
    await updateContentPlan(today.slice(0, -1), 'В планах', taskText);
}

function clearModalPlan() {
    document.getElementById('task-text-plan').value = '';
}


async function updateContentPlan(case_id, case_text, text_task) {
    const contentData = {
        case_id: case_id,
        case_text: case_text,
        text_task: text_task,
    };

    const response = await fetch("/plan_modal", {
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