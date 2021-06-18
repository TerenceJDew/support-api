from flask import Flask, jsonify, request, render_template
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from bson.json_util import dumps, loads

import re

from pymongo.collection import ReturnDocument

app = Flask(__name__)
CORS(app)
app.config[
    "MONGO_URI"
] = "mongodb://root:rooter@vrtual-shard-00-00.wer4d.mongodb.net:27017,vrtual-shard-00-01.wer4d.mongodb.net:27017,vrtual-shard-00-02.wer4d.mongodb.net:27017/bcss_survey?ssl=true&replicaSet=Vrtual-shard-0&authSource=admin&retryWrites=true&w=majority"
mongo = PyMongo(app)
app.config.from_pyfile("settings.py")

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
# // These are fake emails
app.config["MAIL_USERNAME"] = "scoopsshopbigcorp@gmail.com"
app.config["MAIL_PASSWORD"] = "Orchid20?!?!"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)


def send_mail(to, subject, template, **kwargs):
    msg = Message(
        subject=subject, sender="scoopsshopbigcorp@gmail.com", recipients=to.split()
    )
    msg.body = "Please Enjoy Your Free Coupon from BC Scoop Shop"
    msg.html = render_template(template, **kwargs)
    mail.send(msg)


def parse_json(data):
    return loads(dumps(data))


@app.get("/")
def get_home():
    return "Why are you here? This isn't the data you were looking for"


@app.post("/submissions")
def post_answers():
    request_data = request.json
    sanitized_data = parse_json(request_data)
    print(sanitized_data)
    mongo.db.submissions.find_one_and_update(
        {"email": request_data["email"]},
        {"$set": sanitized_data},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    send_mail(request_data["email"], "Your Free Coupon", "coupon.html")
    return request_data


@app.get("/questions")
def get_questions():
    email = request.args["email"]
    content = {
        "treattype": {
            "prompt": "Select your frozen treat of choice:",
            "choices": ["Soft-Serve", "Hard(Scooped)", "Frozen Yogurt"],
        },
        "flavor": {
            "prompt": "Select your favorite flavor",
            "choices": ["Chocolate", "Vanilla", "Twist"],
        },
        "scoopflavor": {
            "prompt": "Select your favorite Scoop flavor",
            "choices": [
                "Chocolate",
                "Vanilla",
                "Strawberry",
                "Mint",
                "Green" "Tea",
            ],
        },
        "cupcone": {
            "prompt": "Select what you like to hold your ice cream",
            "choices": ["Cup", "Cone"],
        },
        "topping": {
            "prompt": "Select your Topping of Choice",
            "choices": ["Sprinkles", "Hot Fudge", "Dip"],
        },
        "dip": {
            "prompt": "Select your Dip Flavor of Choice",
            "choices": ["Chocolate", "Cherry"],
        },
    }

    existing_record = mongo.db.submissions.find_one({"email": email})
    if existing_record is not None:
        del existing_record["_id"]
        content.update({"answers": existing_record})
    print(content)

    return jsonify(content)
