# Business Registration API 1

Этот проект реализует API на FastAPI, которое принимает JSON-запрос с данными регистрации юридических лиц и автоматически заполняет веб-форму на сайте штата (реализован пример для Орегона с использованием Selenium).

## Структура проекта

business-registration-api/ ├── app/ │ ├── init.py │ ├── main.py # FastAPI-приложение │ ├── models.py # Pydantic-модели для валидации входящих данных │ └── selenium_handlers.py # Логика заполнения формы через Selenium (пример для OR) ├── requirements.txt # Зависимости проекта ├── Dockerfile # Docker-конфигурация └── README.md # Инструкция по запуску проекта

bash
Копировать
Редактировать

## Установка и запуск

### Локально (без Docker)

1. Создайте и активируйте виртуальное окружение:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
Установите зависимости:

bash
Копировать
Редактировать
pip install -r requirements.txt
Убедитесь, что у вас установлен Chrome и ChromeDriver.
ChromeDriver должен соответствовать версии установленного Chrome.

Запустите сервер:

bash
Копировать
Редактировать
uvicorn app.main:app --reload
API будет доступно по адресу: http://127.0.0.1:8000/docs

### С использованием Docker
Соберите Docker-образ:

bash
Копировать
Редактировать
docker build -t business-registration-api-1 .
Запустите контейнер:

bash
Копировать
Редактировать
docker run -d -p 8000:8000 business-registration-api-1
API будет доступно по адресу: http://localhost:8000

Пример JSON-запроса
json
Копировать
Редактировать
{
  "credentials": {
    "login": "johndoe123",
    "password": "securepassword123"
  },
  "state": "OR",
  "data": {
    "entityType": "DLLC",
    "entityState": "OR",
    "activityType": "This is a description of the business activity.",
    "company": {
      "name": "Oregon Test LLC",
      "designator": "DLLC",
      "address": {
        "street": "1234 Main St",
        "extra": "",
        "city": "Portland",
        "state": "OR",
        "zipCode": "97201"
      }
    },
    "contact": {
      "firstName": "John",
      "lastName": "Doe",
      "email": "johndoe@example.com",
      "mobile": "5031234567"
    },
    "members": [
      {
        "isIndividual": true,
        "firstName": "Jane",
        "lastName": "Doe",
        "companyName": "",
        "percentOfOwnership": 100,
        "address": {
          "street": "1234 Main St",
          "extra": "",
          "city": "Portland",
          "state": "OR",
          "zipCode": "97201"
        }
      }
    ],
    "agent": {
      "isIndividual": true,
      "firstName": "John",
      "lastName": "Doe",
      "companyName": "",
      "address": {
        "street": "1234 Main St",
        "extra": "",
        "city": "Portland",
        "state": "OR",
        "zipCode": "97201"
      }
    },
    "organizer": {
      "isIndividual": true,
      "firstName": "John",
      "lastName": "Doe",
      "middleName": "Michael",
      "companyName": "",
      "email": "johndoe@example.com",
      "phone": "5031234567",
      "addressStreet": "1234 Main St",
      "addressExtra": "",
      "addressState": "OR",
      "addressCity": "Portland",
      "addressZipCode": "97201",
      "addressCountry": "USA",
      "addressCounty": "Multnomah"
    }
  }
}
Ответ API
При успешном выполнении API вернёт JSON-ответ вида:

json
Копировать
Редактировать
{
  "status": "success",
  "application_id": "123456",
  "state": "OR"
}
В случае ошибки:

json
Копировать
Редактировать
{
  "status": "error",
  "message": "Описание ошибки",
  "state": "OR"
}