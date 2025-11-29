# models.py
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    __table_args__ = (
        UniqueConstraint("name", "age", name="uq_student_name_age"),
        {"mysql_engine": "InnoDB"},
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "age": self.age}


class Course(Base):
    __tablename__ = "courses"
    __table_args__ = (
        UniqueConstraint("title", name="uq_course_title"),
        {"mysql_engine": "InnoDB"},
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    credits = Column(Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "credits": self.credits}
