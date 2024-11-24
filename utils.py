from init import db, app
from models import User, UserRole, Ticket, Door
import hashlib
from sqlalchemy import or_
from datetime import datetime
import requests
import base64


def get_door():
    doors =  Door.query.all()
    json_list = []
    for door in doors:
        json_list.append({
            "door_id": door.id,
            "name": door.name,
            "ipaddress": door.ipaddress
        })
    return json_list

def add_user(name, email, password, avatar_path, address, phonenum, user_role=UserRole.USER, door_id="None"):

    try:
        password = str(hashlib.sha256(password.encode('utf-8')).hexdigest())
        user = User(name=name, email=email, password=password, avatar=avatar_path,
                    user_role=user_role, phone_num=phonenum, address=address)
        ticket= Ticket(use_id=user.id, door_id=door_id)
        db.session.add(user)
        db.session.add(ticket)
        db.session.commit()

        response = requests.get(avatar_path)
        response.raise_for_status()  # Kiểm tra xem có lỗi khi tải ảnh không
        # Chuyển đổi nội dung ảnh sang Base64
        image_base64 = base64.b64encode(response.content).decode('utf-8')

        header = {"X-API-Key": "Ptit@2024ReCognizeFace"}
        payload = {
            "registration_id": user.id,
            "avatar_base64": image_base64,
            "event_id": door_id
        }
        requests.post("https://localhost:8080/api/add_user", headers=header, json=payload)

    except Exception as e:
        print(f"Error committing transaction: {str(e)}")
        db.session.rollback()


def face_recognize(image_base64, door_id):
    header = {"X-API-Key": "Ptit@2024ReCognizeFace"}
    payload = {
        "avatar_base64": image_base64,
        "event_id": door_id
    }
    response = requests.post("https://localhost:8080/api/face_recognize", headers=header, json=payload)

    return response.content


def check_login(email, password):
    if email and password:
        password = str(hashlib.sha256(password.encode('utf-8')).hexdigest())
        user = User.query.filter(User.email.__eq__(email.strip()), User.password.__eq__(password)).first()
        return user


def get_user_by_id(user_id):
    return User.query.get(user_id)


def delete_au(user_id, door_id):
    header = {"X-API-Key": "Ptit@2024ReCognizeFace"}
    payload = {
        "registration_id": user_id,
        "event_id": door_id
    }
    response = requests.post("https://localhost:8080/api/delete", headers=header, json=payload)
    return response

if __name__ == "__main__":
    name = "Nhân admin"
    email = "admin@gmail.com"
    password = "123456"
    avatar_path = "static/image/deafaut_avatar.jpg"
    address = "Yen Nhan"
    phonenum = "01234556"
    #
    user_role = UserRole.ADMIN
    with app.app_context():
        add_user(name=name, email=email, password=password, avatar_path=avatar_path,
                 phonenum=phonenum, address=address, user_role=user_role)

