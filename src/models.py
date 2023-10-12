from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

from .database import Base


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)


class FloorPlan(Base):
    __tablename__ = "floor_plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    original_url = Column(String, unique=True)
    thumb_url = Column(String, unique=True)
    large_url = Column(String, unique=True)
    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="cascade", onupdate="cascade")
    )

    project = relationship(
        "Project", backref=backref("floor_plans", cascade="all,delete-orphan")
    )
