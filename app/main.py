from fastapi import FastAPI
from app.routes.pdf_routes import router as pdf_router

app = FastAPI()

app.include_router(pdf_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
