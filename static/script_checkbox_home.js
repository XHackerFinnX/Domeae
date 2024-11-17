document.querySelectorAll('.task-item input[type="checkbox"]').forEach((checkbox) => {
    checkbox.addEventListener('change', function () {
        const taskId = this.id;

        console.log(taskId);
        updateCheckBox(taskId);
    });
});

async function updateCheckBox(case_id) {
    const contentData = {
        case_id: case_id
    };

    const response = await fetch("/update_checkbox", {
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