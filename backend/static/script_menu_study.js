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
    }

    else if (event.target.matches('.menu-item') && !event.target.classList.contains('has-submenu')) {
        event.target.closest('.dropdown-menu').style.display = 'none';

        console.log(event.target.id, event.target.innerText);
        await updateMenuStudy(event.target.id, event.target.innerText);
    }
});


async function updateMenuStudy(case_id, menu_text) {
    const contentData = {
        case_id: case_id,
        menu_text: menu_text
    };

    const response = await fetch("/update_menu_study", {
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