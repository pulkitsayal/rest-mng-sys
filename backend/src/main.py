from fastapi import FastAPI
from data import Base, engine
from components.login import router as login_router
from components.table import router as table_router
from components.user import router as user_router
from components.menu import router as menu_router
from components.assistance import router as assistance_router
from components.kitchen import router as kitchen_router
from components.waiter import router as waiter_router
from components.feedback import router as feedback_router
from components.category import router as category_router

# FastAPI app instance
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(login_router)
app.include_router(table_router)
app.include_router(user_router)
app.include_router(menu_router)
app.include_router(assistance_router)
app.include_router(kitchen_router)
app.include_router(waiter_router)
app.include_router(feedback_router)
app.include_router(category_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    