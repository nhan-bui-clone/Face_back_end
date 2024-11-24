from flask import render_template, request, redirect, url_for, jsonify, session
from models import *
import utils
import cloudinary.uploader
from flask_login import login_user, logout_user, current_user
from init import login_manager
import replicate
from dotenv import load_dotenv

from utils import face_recognize

load_dotenv()

@app.context_processor
def inject_user_role():
    return dict(UserRole=UserRole)


@app.route("/", methods=['post'])
def home():
    # products = Products.query
    doors = utils.get_door()
    return jsonify(doors)



@app.route("/login", methods=['post'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password", "").strip()
    user = utils.check_login(email=email, password=password)

    if user:
        login_user(user=user)

        return jsonify({"status": "sucess"}), 200

    return  jsonify({"status": "fail"}), 401



@app.route("/register", methods=['get', 'post'])
def register():
    data = request.get_json()
# Lấy các trường từ JSON
    name = data.get("name")
    email = data.get("email")
    password = data.get("password", "").strip()
    cpass = data.get("confirm_password", "").strip()
    address = data.get("address", "").strip()
    phonenum = data.get("phonenum")
    avatar_path = "https://res.cloudinary.com/dscod7nw4/image/upload/v1708148084/qi3ttkumhoogbhew8ae6.jpg"
    avatar = data.get("avatar")

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        avatar_path = res['secure_url']

    if password != cpass:
        return jsonify({"status": "fail"}), 402

    try:
        utils.add_user(name=name, email=email, password=password, avatar_path=avatar_path,
                       address=address, phonenum=phonenum)
        return jsonify({"status": "sucess"}), 200
    except Exception as e:
        return jsonify({"status": "fail"}), 500


@app.route("/delete")
def delete_authentication():
    data = request.get_json()
    user_id = data.get('user_id')
    door_id = data.get('door_id')
    res = utils.delete_au(user_id=user_id, door_id=door_id)
    return res


@app.route("/face_recognize")
def recognize():
    data =  request.get_json()
    avatar = data.get('avatar')
    door_id = data.get('door_id')
    response = utils.face_recognize(image_base64=avatar, door_id=door_id)
    return jsonify(response)

@login_manager.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route("/log-out")
def log_out():
    logout_user()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)