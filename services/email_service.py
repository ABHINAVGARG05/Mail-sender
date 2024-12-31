from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.user import User
from models.mail_data import EmailRecords
from db.database import initialize_db, Config
from flask_mail import Mail, Message
import pandas as pd
import os

def send_bulk_emails(mail, file,template_html):
    current_user = get_jwt_identity()

    if not file:
        return {"message": "No file provided"}, 400

    file_extension = file.filename.split('.')[-1].lower()
    try:
        if file_extension == 'xlsx':
            data = pd.read_excel(file) 
        elif file_extension == 'csv':
            data = pd.read_csv(file)
        else:
            return {"message": "Unsupported file format. Please upload .csv or .xlsx files"}, 400

        required_columns = {'email_id', 'subject'}
        if not required_columns.issubset(data.columns):
            return jsonify({"error": f"CSV must contain the following columns: {required_columns}"}), 400

        if data['email_id'].isnull().sum() > 0:
            return jsonify({"error": "Missing email addresses in the file"}), 400

        for index, row in data.iterrows():
            updated_template = template_html
            for column_name in data.columns[2:]:
                placeholder = f"{{{{ {column_name} }}}}"
                updated_template = updated_template.replace(placeholder, str(row[column_name]))

            msg = Message(
                subject=row['subject'],
                recipients=[row['email_id']],
                sender=os.getenv('MAIL_SENDER')
            )
            print(msg)
            msg.html = updated_template
            mail.send(msg)

            email_record = EmailRecords(
                recipient=row['email_id'],
                subject=row['subject'],
                message=updated_template,
                sender=current_user["username"]
            )
            print(email_record)
            try:
                email_record.save()
            except Exception as e:
                return jsonify({"message":"Error in stroign in db"}), 500

        return jsonify({"message": "Emails sent successfully!"}), 200

    except Exception as e:
        return {"message": f"Error processing file: {str(e)}"}, 500

