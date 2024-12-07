from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.user import User
from mongoengine.errors import DoesNotExist
from db.database import initialize_db, Config
from flask_mail import Mail, Message
import pandas as pd
import os
from flask_cors import cross_origin
from services.auth_services import register_user, login_user
from services.email_service import send_bulk_emails
from models.mail_data import EmailRecords



app = Flask(__name__)

app.config['MAIL_SERVER']=os.getenv('MAIL_SERVER')
app.config['MAIL_PORT']= int(os.getenv('MAIL_PORT',587))
app.config['MAIL_USE_TLS']= os.getenv('MAIL_USE_TLS')== 'True'
app.config['MAIL_USE_SSL']= os.getenv('MAIL_USE_SSL') == 'True'
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY



jwt = JWTManager(app)

initialize_db()


@app.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    response, status_code = register_user(data)
    return jsonify(response),status_code

@app.route('/login',methods = ['POST'])
def login():
    data = request.get_json()
    response, status_code = login_user(data)
    return jsonify(response),status_code


@app.route('/',methods = ['GET'])
def index():
    return render_template('login.html')

@app.route('/upload',methods = ['POST'])
@jwt_required()
def upload():
    current_user = get_jwt_identity()

    if not current_user['isAdmin']:
        return jsonify({"error": "Unauthorized: Admin access required"}), 403

    
    file = request.files.get('file')
    email_id = request.form.get('Email')
    password = request.form.get('Password-Email')
    app.config['MAIL_USERNAME']= email_id
    app.config['MAIL_PASSWORD'] = password
    email = Mail(app)
    return send_bulk_emails(email, file)

@app.route('/get-mails',methods = ['GET'])
@jwt_required()
def get_all_mails():

        emails = EmailRecords.objects()
        results = []

        for record in emails:
                results.append({
                    "recipient": record.recipient,
                    "subject": record.subject,
                    "message": record.message,
                    "sender": record.sender
                })

        return jsonify(results), 200


if __name__ == '__main__':
    app.run(debug = True)