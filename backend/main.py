from fastapi import Depends, File, UploadFile, FastAPI, HTTPException, Request, Form
from sqlalchemy.orm import Session
from datetime import datetime, date, time
import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
import shutil
import os
from PIL import Image


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates("templates")


# Allowed image formats
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/edit/{task_id}")
def edit_task_form(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("edit-task.html", {"request": request, "task": task})


@app.post("/edit/{task_id}")
def update_task(
    request: Request,
    task_id: int,
    subject: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        # Clean and parse date and time
        task_date = datetime.strptime(date, "%Y-%m-%d").date()
        # Ensure time string is in "HH:MM" format
        task_time = datetime.strptime(time[:5], "%H:%M").time()

        # Prepare the task data for updating
        task_data = {
            "subject": subject,
            "title": title,
            "description": description,
            "status": status,
            "date": task_date,
            "time": task_time,
        }

        # Update the task
        updated_task = crud.update_task(db, task_id, task_data)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")

        return RedirectResponse(url="/", status_code=303)
    except ValueError as e:
        print(f"Error parsing date/time: {e}")
        raise HTTPException(
            status_code=400, detail="Invalid date or time format")


@app.get("/", response_model=list[schemas.Task])
def read_items(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return templates.TemplateResponse(name="tasks.html", context={"request": request, "tasks": items})


@app.get("/time-table")
def show_timetable(request: Request):
    timetable_exists = os.path.exists(os.path.join("static", "timetable.png"))

    return templates.TemplateResponse(name="schedule.html", context={"request": request, "imgs": timetable_exists})


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Ensure the uploaded file is an image
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only images are allowed.")

    # Fixed file name for uploaded image
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    # Always save as timetable.png or timetable.jpg, etc.
    save_filename = f"timetable.{file_extension}"
    save_path = os.path.join("static", save_filename)

    # Save the file to the static directory
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Verify the image using Pillow (PIL)
    try:
        img = Image.open(save_path)
        img.verify()  # Will raise an exception if the file is not a valid image
        img.close()   # Close the image to release file resources
    except Exception as e:
        os.remove(save_path)  # Remove the invalid image
        raise HTTPException(
            status_code=400, detail=f"Uploaded file is not a valid image: {e}")

    return RedirectResponse(url="/time-table", status_code=303)


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


if __name__ == '__main__':
    uvicorn.run("main:app")
