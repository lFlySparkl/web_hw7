from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, inspect
from datetime import datetime
from faker import Faker
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:1111@localhost:5432/mydatabase'
db = SQLAlchemy(app)

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable=False)
    students = db.relationship("Student", back_populates="group")

class Student(Base):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    group = db.relationship("Group", back_populates="students")

class Teacher(Base):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(100), nullable=False)
    subjects = db.relationship("Subject", back_populates="teacher")  # Додано зворотний зв'язок

class Subject(Base):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship("Teacher", back_populates="subjects")
    grades = db.relationship('Estimate', back_populates='subject')  # Додано зворотний зв'язок

class Estimate(Base):
    __tablename__ = 'estimates'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    grade = db.Column(db.Integer, nullable=False)
    time_rating = db.Column(db.String(100), nullable=False)
    subject = db.relationship('Subject', back_populates='grades')  # Додано зворотний зв'язок

def create_tables():
    with app.app_context():
        inspector = inspect(db.engine)

        if not inspector.has_table("groups"):
            Base.metadata.create_all(bind=db.engine)

        if not inspector.has_table("students"):
            Base.metadata.create_all(bind=db.engine)

        if not inspector.has_table("teachers"):
            Base.metadata.create_all(bind=db.engine)

        if not inspector.has_table("subjects"):
            Base.metadata.create_all(bind=db.engine)

        if not inspector.has_table("estimates"):
            Base.metadata.create_all(bind=db.engine)

def populate_tables():
    fake = Faker()
    
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()

        # Створюємо 3 групи
        for _ in range(3):
            group = Group(group_name=fake.word())
            session.add(group)

        # Створюємо 30 студентів
        for _ in range(30):
            student = Student(student_name=fake.name(), group_id=random.randint(1, 3))
            session.add(student)

        # Створюємо 5 предметів
        for _ in range(5):
            subject = Subject(subject_name=fake.word(), teacher_id=random.randint(1, 3))
            session.add(subject)

        # Створюємо 3 викладачів
        for _ in range(3):
            teacher = Teacher(teacher_name=fake.name())
            session.add(teacher)

        # Створюємо 20 оцінок для кожного студента за всі предмети
        for student in session.query(Student).all():
            for subject in session.query(Subject).all():
                estimate = Estimate(
                    student_id=student.id,
                    subject_id=subject.id,
                    grade=str(random.randint(1, 10)),
                    time_rating=str(fake.date_time_this_decade())
                )
                session.add(estimate)

        session.commit()

if __name__ == "__main__":
    create_tables()
    populate_tables()
