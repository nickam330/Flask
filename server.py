from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from db import Session, Adv
from erros import HttpError
from schema import CreateAdv, validate

app = Flask("app")
bcrypt = Bcrypt(app)


def hash_password(password: str) -> str:
    password = password.encode()
    password = bcrypt.generate_password_hash(password)
    return password.decode()


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.code
    return response


def get_adv_by_id(adv_id: int) -> Adv:
    adv = request.session.get(Adv, adv_id)
    if adv is None:
        raise HttpError(404, "Advertisement not found")
    return adv


def add_adv(adv: Adv):
    request.session.add(adv)
    try:
        request.session.commit()
    except IntegrityError:
        response = jsonify({"error": "Advertisement already exists"})
        response.status_code = 409
        return response


class AdvView(MethodView):

    def get(self, adv_id: int):

        adv = get_adv_by_id(adv_id)
        return jsonify(adv.dict)

    def post(self):
        json_data = validate(request.json, CreateAdv)
        adv = Adv(
            title=json_data["title"],
            description=json_data["description"],
            owner=json_data["owner"],
            password=hash_password(json_data["password"])
        )
        add_adv(adv)
        return jsonify(adv.id_dict)


    def delete(self, adv_id: int):
        adv = get_adv_by_id(adv_id)
        request.session.delete(adv)
        request.session.commit()
        return jsonify({"status": "deleted"})


adv_view = AdvView.as_view("adv_view")

app.add_url_rule("/advs", view_func=adv_view, methods=["POST"])
app.add_url_rule("/advs/<int:adv_id>", view_func=adv_view, methods=["GET", "DELETE"])


if __name__ == '__main__':
    app.run()
