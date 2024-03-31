# Тестовое задание компании Emphasoft <API для бронирования комнат>

## Запуск приложения

Для клонирования репозитория в локальную директорию ввести команду: 
```
git clone https://github.com/murekswork/booking_solution
cd booking_solution
```
Для запуска контейнеров ввести:
```
docker-compose up --build
```
Приложение будет доступно по адресу:
```
localhost:8000/

```

Для запуска тестов ввести:
```
docker-compose exec web python manage.py test --pattern="test_*.py"
```
## Документация

Документация Swagger будет доступна по адресу:
localhost:8000/swagger

Ход моих мыслей при выполнении работы можно посмотреть по адресу:
https://docs.google.com/document/d/1RuFvbL0F01Zeh-3NolOtJRKV7c48ElJxoUFc8-Lw7xQ/edit?hl=ru

