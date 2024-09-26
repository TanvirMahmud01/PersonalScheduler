from fastapi import Depends, FastAPI, HTTPException, Request, Form
from sqlalchemy.orm import Session
from datetime import datetime, date, time
import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates("templates")

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=list[schemas.Task])
def read_items(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return templates.TemplateResponse(name="tasks.html", context={"request": request, "tasks": items})


@app.post("/delete/{item_id}")
def delete_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    print(f"Received data: item_id={item_id}")
    crud.delete_item(db=db, item_id=item_id)
    return RedirectResponse(url="/", status_code=303)


@app.get("/create-task/")
def read_root(request: Request, user_id=1):

    return templates.TemplateResponse(name="new-task.html", context={"request": request, "user_id": user_id})


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Task)
# def create_item_for_user(
#     user_id: int, item: schemas.TaskCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.post("/users/{user_id}/items/")
def create_item(user_id: int, subject: str = Form(...), task: str = Form(...), description: str = Form(...), dueDate: str = Form(...), dueTime: str = Form(...), db: Session = Depends(get_db)):

    try:
        # Convert date and time strings to appropriate types

        task_date = datetime.strptime(dueDate, "%Y-%m-%d").date()
        task_time = datetime.strptime(dueTime, "%H:%M").time()
        print(task_date)
        # Create the item
        item_data = {
            "subject": subject,
            "title": task,
            "description": description,
            "status": "pending",
            "date": task_date,
            "time": task_time
        }

        crud.create_user_item(db=db, item=item_data, user_id=1)
        return RedirectResponse(url="/", status_code=303)

    except Exception as e:
        print(e)
        return {"message": "An error occurred"}
