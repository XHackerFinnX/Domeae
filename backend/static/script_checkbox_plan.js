let taskId;
let checkbox_id
let text_label

document.querySelectorAll('.task-item input[type="checkbox"]').forEach((checkbox) => {
    checkbox.addEventListener('change', function () {
        taskId = this.id;
        const modalOverlayInput = document.querySelector(`.task-container[data-id="${taskId}"]`);
        const taskContainer = modalOverlayInput.closest('.task-container');
        checkbox_id = document.querySelector(`#${taskContainer.getAttribute('data-id')}`);

        text_label = document.querySelector(`label[for="${checkbox_id.id}"]`);

        if (this.checked) {
            // Открываем модальное окно при активации чекбокса
            const modalu = document.getElementById("modal-main");
            modalu.style.display = modalu.style.display === "none" || modalu.style.display === "" ? "flex" : "none";
        }
    });
});

// Логика управления модальными окнами
document.addEventListener("DOMContentLoaded", () => {
    const modals = document.querySelectorAll(".modal-overlay-o");

    modals.forEach(modal => {
        modal.addEventListener("click", (e) => {
            if (e.target.classList.contains("modal-back-o")) {
                // Закрываем текущее окно и возвращаемся в основное
                modal.style.display = "none";
                document.getElementById("modal-main").style.display = "flex";
            } else if (e.target.classList.contains("modal-btn")) {
                const nextModal = e.target.getAttribute("data-next");

                if (e.target.id === '') {
                    console.log("Пусто");
                }
                else {
                    const case_id = e.target.id;
                    console.log(taskId, case_id, text_label.textContent.trim());
                    closeModal(checkbox_id);
                    updateCheckBox(taskId, case_id, text_label.textContent.trim());
                }

                if (nextModal) {
                    // Закрываем текущее окно и открываем следующее
                    modal.style.display = "none";
                    document.getElementById(nextModal).style.display = "flex";
                }
            }
        });
    });
});

document.querySelectorAll('.modal-overlay-o').forEach(overlay => {
    overlay.addEventListener('click', function (event) {

        if (event.target === overlay) { // Проверяем, клик был именно на фоне
            closeModal(checkbox_id);
        }
    });
});

function closeModal(che_id) {
    const modalu = document.getElementById("modal-main");
    const modalu_h = document.getElementById("modal-home");
    const modalu_s = document.getElementById("modal-shopping");
    const modalu_st = document.getElementById("modal-study");
    modalu.style.display = "none";
    modalu_h.style.display = "none";
    modalu_s.style.display = "none";
    modalu_st.style.display = "none";
    che_id.checked = false;
}

async function updateCheckBox(case_id, task_id, text_case) {

    console.log(task_id, case_id)
    const contentData = {
        case_id: case_id,
        task_id: task_id,
        text_case: text_case
    };

    const response = await fetch("/update_checkbox_plan", {
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