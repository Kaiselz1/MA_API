from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, get_db
from api.user import user_router, user_model as model
from api.auth import auth_router
from api.product import product_router
from api.category import category_router
from api.order import order_router
from utils import token_cleanup

app = FastAPI(title="MA API", debug=True)

# Enable for Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, OPTIONS...)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def root():
    return RedirectResponse(url="http://127.0.0.1:8000/docs")

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# making the table
model.User.metadata.create_all(engine)

# Token Cleanup Task
@app.on_event("startup")
@repeat_every(seconds=60*60)  # every hour
def cleanup_tokens_task() -> None:
    db = next(get_db())
    token_cleanup.cleanup_expired_tokens(db)

# Including Routers
app.include_router(auth_router.router)
app.include_router(product_router.router)
app.include_router(category_router.router)
app.include_router(user_router.router)
app.include_router(order_router.router)