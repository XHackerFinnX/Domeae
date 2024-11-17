let item_id;

document.addEventListener('click', async function(event) {

    if (event.target.matches('.icon-list[data-toggle="dropdown"]')) {
        const taskContainer = event.target.closest('.task-container');
        const dropdownMenu = taskContainer.querySelector('.dropdown-menu');
        
        dropdownMenu.style.display = dropdownMenu.style.display === 'none' ? 'block' : 'none';

        document.addEventListener('click', function closeDropdown(e) {
            if (!e.target.closest('.dropdown-menu') && !e.target.closest('.icon-list')) {
                dropdownMenu.style.display = 'none';
                document.removeEventListener('click', closeDropdown);
            }
        });
    }

    const idParts = event.target.id.split("-");
    const lastElement = idParts[idParts.length - 1];

    // Открытие модального окна для переназначения пользователя
    if (event.target.matches('.menu-item') && lastElement === '1') {
        const modalWrapper = document.querySelector('.ModalWrapper');
        modalWrapper.style.display = 'block';  // Показ модального окна

        item_id = event.target.id;

        event.target.closest('.dropdown-menu').style.display = 'none';

        // Закрытие модального окна при клике вне его области
        document.addEventListener('click', function closeModal(e) {
            if (!e.target.closest('.modal-assignee-wrapper') && !e.target.matches('.menu-item')) {
                modalWrapper.style.display = 'none';
                document.removeEventListener('click', closeModal);
            }
        });
    }

    else if (event.target.matches('.menu-item') && !event.target.classList.contains('has-submenu')) {
        event.target.closest('.dropdown-menu').style.display = 'none';

        const textp = document.querySelector('.task-item')
        const textpText = textp.querySelector('label p').innerText;
        //showNotification(textpText);

        console.log(event.target.id, event.target.innerText);
        await updateMenuHome(event.target.id, event.target.innerText);
    }

    // Закрытие модального окна при нажатии на кнопку
    if (event.target.matches('.modalassigneeButton')) {
        const modalWrapper = document.querySelector('.ModalWrapper');
        modalWrapper.style.display = 'none';

        const selectElement = document.getElementById('modal-assignee');
        const selectedValue = selectElement.value;

        console.log(item_id, selectedValue);

        const textp = document.querySelector('.task-item')
        const textpText = textp.querySelector('label p').innerText;
        //showNotification(textpText);

        await updateMenuHome(item_id, selectedValue);
    }

    if (event.target.matches('.has-submenu')) {
        const submenu = event.target.querySelector('.submenu');
        submenu.style.display = submenu.style.display === 'none' ? 'block' : 'none';
    }
    
    if (event.target.matches('.submenu-item')) {
        event.target.closest('.submenu').style.display = 'none';
        event.target.closest('.dropdown-menu').style.display = 'none';

        const textp = document.querySelector('.task-item')
        const textpText = textp.querySelector('label p').innerText;
        //showNotification(textpText);

        console.log(event.target.id, event.target.innerText);
        await updateMenuHome(event.target.id, event.target.innerText);
    }
});


async function updateMenuHome(case_id, menu_text) {
    const contentData = {
        case_id: case_id,
        menu_text: menu_text
    };

    const response = await fetch("/update_menu", {
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

function showNotification(taskText) {
    if (Notification.permission === "granted") {
        const notification = new Notification("Изменено:", {
            body: `${taskText}`
        });

        notification.onclick = () => {
            window.location.href = "/home";
        };
    }
}