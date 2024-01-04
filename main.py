from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from api import schemas, crud
from api.routes import router as api_router
from database.connection import SessionLocal
app = FastAPI()
app.include_router(api_router, prefix="/api")
templates = Jinja2Templates(directory="frontend/templates")
# app.add_middleware(SessionMiddleware, secret_key=None)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
@app.get("/protected/")
def protected_route( request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")


    return {"message": "Welcome to protected route"}