from fastapi import Depends, FastAPI, HTTPException, status, Path
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get(
    "/users/{user_id}/projects/{project_id}/activities/", 
    response_model=list[schemas.Activity], 
    tags=["Actividades"],
    summary= "Listar actividades",
    description= "Permite obtener las actividades dado un usuario y meta.",
)
def list_activities(
    user_id: str = Path(...,description= "UUID del usuario", example = "b9e605ee-4cca-400e-99c5-ae24abca97d5"), 
    project_id: str = Path(...,description= "UID de la meta", example = "016fe969-4d2f-43f9-81b4-1bdcebd975e4"),
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    items = crud.list_activities(db, user_id=user_id, project_id=project_id, skip=skip, limit=limit)
    return items

@app.post(
    "/users/{user_id}/projects/{project_id}/activities/", 
    response_model=schemas.Activity,
    status_code=status.HTTP_201_CREATED, 
    tags=["Actividades"],
    summary= "Crear actividad",
    description= "Permite crear una actividad dado un usuario y meta.",   
)
def create_activity(
    activity: schemas.ActivityCreate,
    db: Session = Depends(get_db),
    user_id: str = Path(...,description= "UUID del usuario", example = "b9e605ee-4cca-400e-99c5-ae24abca97d5"), 
    project_id: str = Path(...,description= "UID de la meta", example = "016fe969-4d2f-43f9-81b4-1bdcebd975e4")
):
    return crud.create_activity(db=db, activity=activity, user_id=user_id, project_id=project_id)

@app.get(
    "/users/{user_id}/projects/{project_id}/activities/{activity_id}", 
    response_model=schemas.Activity, 
    tags=["Actividades"],
    summary= "Ver detalle de actividad",
    description= "Permite obtener el detalle de la actividad."
)
def get_activity(
    user_id: str = Path(...,description= "UUID del usuario", example = "b9e605ee-4cca-400e-99c5-ae24abca97d5"), 
    project_id: str = Path(...,description= "UuID de la meta", example = "016fe969-4d2f-43f9-81b4-1bdcebd975e4"),
    activity_id: str = Path(...,description= "UuID de la actividad", example = "017fe969-4d2f-43f9-81b4-1bdcebd975e4"), 
    db: Session = Depends(get_db)
):
    return crud.get_activity(db, user_id=user_id, project_id=project_id, activity_id=activity_id)

@app.patch(
    "/users/{user_id}/projects/{project_id}/activities/{activity_id}", 
    response_model=schemas.Activity, 
    tags=["Actividades"],
    summary= "Actualizar actividad parcialmente. Forma 1",
    description= "Permite actualizar la actividad parcialmente."
)
def update_activity_patch(
    activity:schemas.ActivityUpdate, 
    db: Session = Depends(get_db),
    user_id: str = Path(...,description= "UUID del usuario", example = "b9e605ee-4cca-400e-99c5-ae24abca97d5"), 
    project_id: str = Path(...,description= "UUID de la meta", example = "016fe969-4d2f-43f9-81b4-1bdcebd975e4"),
    activity_id: str = Path(...,description= "UUID de la actividad", example = "017fe969-4d2f-43f9-81b4-1bdcebd975e4")
):
    return crud.update_activity(db, activity=activity, user_id=user_id, project_id=project_id, activity_id=activity_id)

@app.put(
    "/users/{user_id}/projects/{project_id}/activities/{activity_id}", 
    response_model=schemas.Activity, 
    tags=["Actividades"],
    summary= "Actualizar actividad parcialmente. Forma 2",
    description= "Permite actualizar la actividad parcialmente."
)
def update_activity_put(
    activity:schemas.ActivityBase, 
    db: Session = Depends(get_db),
    user_id: str = Path(...,description= "UUID del usuario", example = "b9e605ee-4cca-400e-99c5-ae24abca97d5"), 
    project_id: str = Path(...,description= "UUID de la meta", example = "016fe969-4d2f-43f9-81b4-1bdcebd975e4"),
    activity_id: str = Path(...,description= "UUID de la actividad", example = "017fe969-4d2f-43f9-81b4-1bdcebd975e4"),
):
    return crud.update_activity(db, activity=activity, user_id=user_id, project_id=project_id, activity_id=activity_id)