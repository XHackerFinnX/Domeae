document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const addButton = document.getElementById('addButton');
    const peopleList = document.getElementById('peopleList');
    const userCount = document.getElementById('userCount');  // Элемент для отображения количества пользователей
    let people = [];  // Массив для хранения людей

    // Функция для получения людей с сервера
    async function fetchPeople() {
        const response = await fetch('/people/name', {
            method: 'POST',  // Устанавливаем метод как POST
            headers: {
                'Content-Type': 'application/json',  // Указываем, что отправляем/получаем JSON
            }
        });

        const data = await response.json();  // Преобразуем ответ в JSON
        people = data;  // Сохраняем полученные данные
        renderPeople(people);  // Отображаем людей на странице
        updateUserCount();  // Обновляем количество пользователей
    }

    // Функция для рендеринга людей
    function renderPeople(filteredPeople) {
        peopleList.innerHTML = '';  // Очищаем текущий список
        filteredPeople.forEach(person => {
            const li = document.createElement('li');
            li.textContent = person[1];  // Имя человека
            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Delete';
            deleteBtn.classList.add('delete-btn');
            deleteBtn.id = `delete-btn-${person[0]}`;  // Устанавливаем уникальный ID для кнопки

            // Добавляем обработчик события для кнопки удаления
            deleteBtn.addEventListener('click', () => deletePerson(person[0]));

            li.appendChild(deleteBtn);
            peopleList.appendChild(li);
        });
    }

    // Функция для добавления человека
    async function addPerson(name) {
        if (name.trim()) {  // Проверяем, чтобы имя не было пустым
            const response = await fetch('/people/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name })  // Отправляем JSON с именем
            });

            if (response.ok) {
                fetchPeople();  // После добавления обновляем список людей
            } else {
                alert('Error adding person');
            }
        }
    }

    // Функция для удаления человека
    async function deletePerson(personId) {
        const response = await fetch(`/people/${personId}`, {
            method: 'DELETE',  // Удаление по ID
        });

        if (response.ok) {
            fetchPeople();  // После удаления обновляем список людей
        } else {
            alert('Error deleting person');
        }
    }

    // Функция для поиска людей
    function searchPeople(query) {
        query = query.toLowerCase();  // Приводим запрос к нижнему регистру
        const filteredPeople = people.filter(person =>
            person[1].toLowerCase().startsWith(query)  // Ищем по имени (person[1])
        );
        renderPeople(filteredPeople);  // Рендерим отфильтрованный список
        updateUserCount(filteredPeople.length);  // Обновляем количество пользователей
    }

    // Обновляем количество пользователей
    function updateUserCount() {
        userCount.textContent = `Количество пользователей: ${people.length}`;
    }

    // Обработчик нажатия на кнопку добавления
    addButton.addEventListener('click', () => {
        addPerson(searchInput.value);  // Добавляем человека, используя текст из input
        searchInput.value = '';  // Очищаем input после добавления
    });

    // Обработчик ввода в поле поиска
    searchInput.addEventListener('keyup', (e) => {
        const inputValue = searchInput.value.trim();
        if (e.key === 'Enter' && inputValue) {
            addPerson(inputValue);  // Если нажата клавиша Enter, добавляем человека
        } else {
            searchPeople(inputValue);  // В другом случае фильтруем список людей
        }
    });

    // Загружаем список людей при инициализации страницы
    fetchPeople();  // Загружаем людей при загрузке страницы
});
