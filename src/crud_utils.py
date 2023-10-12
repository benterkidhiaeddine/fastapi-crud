from sqlalchemy.orm import Session
from . import schemas, models


# get Project by Id
def get_project_by_id(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


# get Project by name
def get_project_by_name(db: Session, project_name: str):
    return db.query(models.Project).filter(models.Project.name == project_name).first()


# add Project to database
def add_project(db: Session, project: schemas.ProjectCreate) -> models.Project | None:
    # create the project model based on the project schema coming from the post request
    new_project = models.Project(name=project.name)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


# Delete project from database
def delete_project(db: Session, project_id: int):
    db.query(models.Project).filter(models.Project.id == project_id).delete()
    db.commit()


# add floor plan
def add_floor_plan(db: Session, project: models.Project, floor_plan_name: str):
    # create new floor plan model
    new_floor_plan = models.FloorPlan(name=floor_plan_name)
    project.floor_plans.append(new_floor_plan)
    db.add(new_floor_plan)
    db.commit()
    db.refresh(project)
    return new_floor_plan
