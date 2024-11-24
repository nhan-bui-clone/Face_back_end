import os
from sqlalchemy import Integer, Column, String, Boolean, DateTime, Enum
from flask_login import UserMixin
from init import db, app
from datetime import datetime
from enum import Enum as UserEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Door(db.Model):
    __tablename__ = "door"
    __table_args__ = {'extend_existing': True}  # Thêm option extend_existing=True

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    ipaddress = Column(String(200), default="No description")

    def __str__(self):
        return f"{self.id} {self.name}"


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class User(db.Model, UserMixin):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    avatar = Column(String(300))
    role = Column(Enum(UserRole), default=UserRole.USER)
    address = Column(String(100), nullable=False)
    phone_num = Column(String(20), nullable=False)

    def __str__(self):
        return self.name


class Ticket(db.Model):
    __tablename__ = "ticket"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    door_id = Column(Integer, ForeignKey('door.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    door = relationship("Door", backref="related_ticket")
    user = relationship("User", backref="related_ticket")
    content = Column(String(1000), default="")
    time_comment = Column(DateTime, default=datetime.now())


if __name__ == "__main__":
    # filenames = os.listdir("static/image")
    # print(filenames)
    with app.app_context():
        # db.session.query(Comment).delete()
        # db.session.query(Cart).delete()
        # db.session.query(Products).delete()
        # db.session.commit()
        db.create_all()
        db.session.commit()

