создаем контейнер
docker run --name my_postgres_container -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=1111 -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres

запускаем контейнер
docker start my_postgres_container

запускаем "main.py" для создания и наполнения таблиц

далее проверяем sql или из файла "my_select.py" только передавая цифру main(1) # Для виклику функцій змініть тільки "1" на потрібний вам від 1 до 12.