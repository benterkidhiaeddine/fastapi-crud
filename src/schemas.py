from pydantic import BaseModel
import json


class FloorPlanBase(BaseModel):
    name: str


class FloorPlanCreate(FloorPlanBase):
    pass


class FloorPlan(FloorPlanBase):
    id: int
    original_url: str
    thumb_url: str
    large_url: str
    project_name: str

    class Config:
        orm_mode = True


# the Project schema that is going to be accepted in the api endpoint


class ProjectBase(BaseModel):
    name: str


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    floor_plans: list[FloorPlanBase] = []

    class Config:
        orm_mode = True
