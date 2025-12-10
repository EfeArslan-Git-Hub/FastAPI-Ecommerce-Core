from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from .database import engine, Base
from .routers import products, orders

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Ecommerce Core by Efe Arslan",
    description="A simple REST API for managing products and orders with stock management.",
    version="1.0.0"
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>FastAPI Ecommerce</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
                .portfolio-btn {
                    position: absolute;
                    top: 20px;
                    left: 20px;
                    background-color: #333;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    transition: background-color 0.3s;
                }
                .portfolio-btn:hover { background-color: #555; }
                .content { text-align: center; margin-top: 100px; }
            </style>
        </head>
        <body>
            <a href="https://efe-arslan-portfolio.vercel.app/" class="portfolio-btn" target="_blank">Portfolio</a>
            <div class="content">
                <h1>Welcome to the FastAPI Ecommerce Core API</h1>
                <p>Visit <a href="/docs">/docs</a> for API documentation.</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
