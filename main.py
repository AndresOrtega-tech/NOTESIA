from backend.app.main import app

# Este archivo sirve como punto de entrada para Vercel
# Importa la aplicación FastAPI desde backend/app/main.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)