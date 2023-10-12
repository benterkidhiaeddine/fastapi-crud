from fastapi import Depends, HTTPException, UploadFile, Form, File
from sqlalchemy.orm import Session
import os


from .database import SessionLocal, engine
from . import app, schemas, models, crud_utils

# Create the database schema
models.Base.metadata.create_all(bind=engine)


# Configure the upload directory

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
UPLOAD_PATH = os.path.join(BASE_PATH, "uploads")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return {"message": "Hello world"}


@app.post("/projects/", response_model=schemas.Project)
def post_projects(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = crud_utils.get_project_by_name(db=db, project_name=project.name)
    if db_project:
        raise HTTPException(
            status_code=400, detail="A project with this name already Exists"
        )
    return crud_utils.add_project(db=db, project=project)


@app.get("/projects/{project_id}", response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud_utils.get_project_by_id(db=db, project_id=project_id)
    if not db_project:
        raise HTTPException(
            status_code=404, detail="A project with this id does not exist"
        )
    return db_project


@app.post("/projects/{project_id}/floor_plans/")
def upload_floor_plans(
    project_id: int,
    db: Session = Depends(get_db),
    floor_plan_name: str = Form(...),
    uploaded_file: UploadFile = File(...),
):
    # check if there was an uploaded file
    if not uploaded_file:
        return {"message": "No upload file sent"}
    # check if the project exists
    db_project = crud_utils.get_project_by_id(db=db, project_id=project_id)
    if not db_project:
        raise HTTPException(
            status_code=404,
            detail="You can't add a floor plan to a project that does not exist",
        )

    # Define the upload directory based on project_id
    upload_folder = os.path.join(UPLOAD_PATH, f"originals/{project_id}")
    # if path not exist of the folder of the project create it else continue normally
    if not os.path.exists(upload_folder):
        print("does not exist")
        os.mkdir(upload_folder)

    # save the uploaded file in a specific directory : the directory with the project id in ./uploads/originals/{project_id}
    file_upload_location = os.path.join(upload_folder, uploaded_file.filename)
    with open(file_upload_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    # create the different versions of the uploaded photo and save them

    # create the floorPlan Object and store it in the database with necessary information
    new_floor_plan = crud_utils.add_floor_plan(
        db=db, project=db_project, floor_plan_name=floor_plan_name
    )

    return new_floor_plan


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    crud_utils.delete_project(project_id=project_id, db=db)
    return {"deleted": " deleted"}
