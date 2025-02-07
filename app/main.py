from fastapi import FastAPI, HTTPException
from app.models import RequestResponse
from app import selenium_handlers

app = FastAPI(title="Business Registration API")

@app.post("/register")
async def register_business(response: RequestResponse):
    """
    Принимает JSON с данными регистрации, валидирует их и заполняет форму на сайте.
    Возвращает {"status": "success", "response": "...", "state": "..."} или сообщение об ошибке.
    """

    # Запуск функции для выбранного штата
    response_data = selenium_handlers.fill_form(response.state, response.credentials, response.data)
        
    # Ответ в формате JSON
    return {"status": "success", "response": response_data, "state": response.state.upper()}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
