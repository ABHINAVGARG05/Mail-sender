from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.user import User
from models.mail_data import EmailRecords
from db.database import initialize_db, Config
from flask_mail import Mail, Message
import pandas as pd
import os

def send_bulk_emails(mail, file):
    current_user = get_jwt_identity()
    if file and file.filename.endswith('.csv'):
        csv = pd.read_csv(file)

        if csv['email_id'].isnull().sum() != 0:
            return "Error: Missing values in CSV", 400

        for _, row in csv.iterrows():
            msg = Message(
                subject = str(row['subject']),
                recipients=[row['email_id']],
                sender= os.getenv('MAIL_SENDER')
            )
            msg.body = str(row.get('message'))
            mail.send(msg)
            email_record = EmailRecords(
                recipient=str(row['email_id']),
                subject=str(row['subject']),
                message=str(msg.body),
                sender=current_user["username"]
            )
            email_record.save()
        
        return {"message":"Emails sent successfully!"}, 200
    return {"message":"Invalid file format"}, 400
