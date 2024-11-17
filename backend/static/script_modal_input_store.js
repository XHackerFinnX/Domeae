document.querySelectorAll('.task-item input[type="checkbox"]').forEach((checkbox) => {
    checkbox.addEventListener('change', function () {
        const taskId = this.id;
        const modalOverlayInput = document.querySelector(`.task-container[data-id="${taskId}"] .modalOverlayInput`);
        const textInput = modalOverlayInput.querySelector('.modaltextInput');

        const taskContainer = modalOverlayInput.closest('.task-container');
        const checkbox = document.querySelector(`#${taskContainer.getAttribute('data-id')}`);

        if (modalOverlayInput) {
            // Показываем модальное окно, если чекбокс включен
            modalOverlayInput.style.display = this.checked ? 'block' : 'none';
        } else {
            console.error(`Modal overlay not found for checkbox with id: ${taskId}`);
        }

        // Ограничение на ввод только чисел
        textInput.addEventListener('input', () => {
            textInput.value = textInput.value.replace(/[^0-9]/g, '');  // Удаляет все нечисловые символы
        });

        // Закрытие окна при клике вне модального окна
        modalOverlayInput.addEventListener('click', (e) => {
            if (e.target === modalOverlayInput) {
                textInput.value = "";
                closeModal(modalOverlayInput, checkbox);
            }
        });

    });
});

// Закрытие модального окна при клике на кнопку подтверждения
document.querySelectorAll('.modalconfirmButton').forEach((button) => {
    button.addEventListener('click', async function () {
        const modalOverlayInput = this.closest('.modalOverlayInput');
        if (modalOverlayInput) {
            const textInput = modalOverlayInput.querySelector('.modaltextInput');

            modalOverlayInput.style.display = 'none';
            // Найти и отключить связанный чекбокс
            const taskContainer = modalOverlayInput.closest('.task-container');
            if (taskContainer) {
                const checkbox = document.querySelector(`#${taskContainer.getAttribute('data-id')}`);

                console.log("Значение из textarea:", textInput.value);
                console.log(checkbox.id);

                await updateCheckBoxStore(checkbox.id, textInput.value);

                textInput.value = "";
            }
        } else {
            console.error("Modal overlay not found for confirm button");
        }
    });
});


// Функция закрытия модального окна
function closeModal(moi, cb) {
    moi.style.display = 'none';
    cb.checked = false;  // Сбрасываем чекбокс
}

async function updateCheckBoxStore(case_id, sum_pay) {
    const contentData = {
        case_id: case_id,
        sum_pay: sum_pay
    };

    const response = await fetch("/update_checkbox_store", {
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