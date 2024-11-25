# Domeae

## Мой собственный сайт реализованный на фреймворке **FastApi**.

### На сайте реализована авторизация по **session**, использование базы данных **PostgreSQL**, **api telegram** для отправки уведомлений о создании и изменение задач.
---

### На данном сайте можно создавать задачи, назначать их пользователям, ставить дедлайн, приоритеты и тд. 

### Есть 4 блока для задач:
### 1. Дом
### 2. Покупки
### 3. Учеба
### 4. В планах

![Меню](https://github.com/XHackerFinnX/Domeae/blob/master/picture_readme/menu.png)

### Также есть фильтры на задачи (Сегодня, С флажком, Назначено) с помощью которых удобно ориентироваться по задачам. 

![Фильтры](https://github.com/XHackerFinnX/Domeae/blob/master/picture_readme/filter.png)

### Также можно просмотреть свои завершенные задачи и при необходимости почистить историю завершенных задач. 

![Завершено история](https://github.com/XHackerFinnX/Domeae/blob/master/picture_readme/history.png)

### В блоке "В планах" можно создать "план" и потом переместить в один из 3 блоков (Дом, Покупки, Учеба)

![В планах](https://github.com/XHackerFinnX/Domeae/blob/master/picture_readme/plane.png)

### Дом, Покупки, Учеба - разделены на группы

## Дом
![Дом](https://github.com/XHackerFinnX/Domeae/blob/master/picture_readme/home.png)

## Покупки
![Покупки](https://github.com/XHackerFinnX/Domeae/blob/master/picture_readme/store.png)

## Учеба
![Учеба](https://github.com/XHackerFinnX/Domeae/blob/master/picture_readme/study.png)

### В блоках "Дом" и "Покупки" есть меню у каждой задачи. В блоке "Учеба" и "В планах" меню другие.

### Меню "Дом" и "Покупки"

![МенюДП](https://github.com/XHackerFinnX/Domeae/blob/master/picture_readme/%D0%BC%D0%B5%D0%BD%D1%8E%D0%B4%D0%BF.png)

### Меню "Учеба"

![МенюУ](https://github.com/XHackerFinnX/Domeae/blob/master/picture_readme/%D0%BC%D0%B5%D0%BD%D1%8E%D1%83.png)

### "В планах" только удалить "план"

## Создание самих задач в **блоках**
### В блоках "Дом" и "Покупки" создание задачи одинаковы. При создании задачи указывается:
### 1. Название задачи
### 2. Поставить напоминание или нет
### 3. Кому назначить задачу

![Создание задачи](https://github.com/XHackerFinnX/Domeae/blob/master/picture_readme/%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0.png)

### В блоке "Покупки" реализовано ИТОГО. При нажатии на задачу, чтобы её завершить вылезает окошко куда нужно вписать сумму, которую потратили

![Сумма](https://github.com/XHackerFinnX/Domeae/blob/master/picture_readme/%D0%A1%D1%83%D0%BC%D0%BC%D0%B0.png)

### При вводе суммы и нажатии на кнопку. Задача завершается и в ИТОГО добавляется сумма потраченная в этом месяце. Каждый месяц сумма обнуляется и в базе данных хранится история потраченных денег за каждый месяц
