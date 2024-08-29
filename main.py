from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import *
from templating import TemplateResponse
import hashlib
from starlette.templating import Jinja2Templates

Base.metadata.create_all(bind= engine)
app = FastAPI()

templates = Jinja2Templates(directory='templates')
TemplateResponse = templates.TemplateResponse

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/games/', name = 'games:page_games', response_class = HTMLResponse)
def games_page(request: Request, db: Session = Depends(get_db)):
    games = db.query(Game).all()
    context = {
        'games' : games
    }
    return TemplateResponse(request = request, name = "games_page.html", context = context)

@app.get('/games/{id}', name = 'games:page_games', response_class = HTMLResponse)
def games_page(id, request: Request, db: Session = Depends(get_db)):
    games = db.query(Game).filter_by(id = id).first()
    print(games.id)
    context = {
        'games': games
    }
    return TemplateResponse(request = request, name = "games_page.html", context = context)


@app.get("/registration/", name = "registration:page_registration", response_class = HTMLResponse)
def registration_page(request: Request):
    return TemplateResponse(request = request, name = "registration_page.html")


@app.post("/registration/", name = "registration:page_registration", response_class = HTMLResponse)
def registration_buyers_page(request: Request, username: str = Form(), password: str = Form(), repeat_password: str = Form(),
                           age: int = Form(), db: Session = Depends(get_db)):
    users = set()
    username = username
    password = password
    repeat_password = repeat_password
    age = age
    buyers = db.query(Buyer).all()
    info = {}
    for buyer in buyers:
        users.add(buyer.name)
    if username in users:
        info['error'] = 'Такой пользователь уже зарегистрирован'
        return TemplateResponse(request=request, name="registration_page.html", context=info)
    elif repeat_password != password:
        info['error'] = 'Пароли не совпадают'
        return TemplateResponse(request=request, name="registration_page.html", context=info)
    elif int(age) < 18:
        info['error'] = 'Вы должны быть старше 18'
        return TemplateResponse(request=request, name="registration_page.html", context=info)
    else:
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        buyer = Buyer(username=username, hashed_password=hashed_password)
        db.add(buyer)
        db.commit()
        return TemplateResponse(request=request, name="registration_page.html",
                                context={'wellcome': f'вы зарегистрированы'})


@app.post("/Game/")
def creat_Game(id: int, title: str, cost: int, size: int, description: str, age_limited: int, db: Session = Depends(get_db)):
    games = Game(id = id, title = title, cost = cost, description = description, age_limited = age_limited)
    db.add(games)
    db.commit()
    return "Новая игра"

@app.get("/Game/")
def read_Game(db: Session = Depends(get_db)):
    games = db.query(Game).all()
    return games


@app.put("/Game")
def update_Game(id: int, title: str, cost: int, size: int, description: str, age_limited: int, db: Session = Depends(get_db)):
    games = db.query(Game).filter(Game.id == id).first()
    if games is not None:
        games.title = title
        games.cost = cost
        games.description = description
        games.size = size
        games.age_limited = age_limited
        db.commit()
        new_games = db.query(Game).filter(Game.id == id).first()
        return f'Игра обновлена {new_games}'
    else:
        return f'Игр с таким id {id} не существует'

@app.delete("/Game/")
def delete_Game(id: int, db: Session = Depends(get_db)):
    games = db.query(Game).filter(Game.id == id).first()
    db.delete(games)
    db.commit()
    return 'Игра удалена успешно'


