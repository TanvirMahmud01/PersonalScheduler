from sqlalchemy.orm import Session

import models
import schemas


def update_task(db: Session, task_id: int, task_data: dict):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return None
    for key, value in task_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).order_by(models.Task.date, models.Task.time).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.TaskCreate, user_id: int):
    db_item = models.Task(**item, owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    try:
        db.query(models.Task).filter(models.Task.id == item_id).delete()
        db.commit()
    except:
        return {"message": "Item not found"}
    return {"message": "Item deleted successfully"}
