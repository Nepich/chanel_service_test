# chanel_service_test

Проект который позволяет получать данные о заказах из гугл-таблицы 

(https://docs.google.com/spreadsheets/d/1UfcLP36X-Oe3mgjHJOQUU3nvJMLlKWJQwuLjKmlxMJg/edit?usp=sharing), 

и перенести данные в PostgreSQL с добавлением стоимсоти заказа в рублях по курсу ЦБ РФ 
с обновлением этого столбца в режиме реального времени и проверкой срока поставки. В случае истечения срока поставки приходит уведомление в чат-бота телеграмм https://t.me/chanel_service_test_bot.

Войдите в бота и нажмите `/start`

Для использования Вам потребуется установить Docker и Docker-compose на локальной машине.

После скачивания проекта и установки необходимого ПО, находясь в корневом каталоге проекта, в терминале запустите команду `docker-compose up -d`
Докер сделает все за Вас. 

База данных работает на порту ___5432___

Для получения UI интерфеса в строке адреса браузера введите http://localhost:5050/ или кликнете на ссылку.

Для входа используйте логин `user@user.com` пароль `chanel_service_1234`

Далее подключите базу данных. В полях: 
- **Host name** укажите `postgres`
- **Maintenance database** укажите `chanel_service`
- **Username** укажите `postgres`
- **Password** укажите `chanel_service_1234`

и нажмите `Save`

![Alt-текст](https://habrastorage.org/r/w1560/getpro/habr/upload_files/af8/32e/31d/af832e31df72441e9f966f8703561975.png "Подключение")
