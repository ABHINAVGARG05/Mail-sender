from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.user import User
from models.mail_data import EmailRecords
from db.database import initialize_db, Config
from flask_mail import Mail, Message
import pandas as pd
import os

def send_bulk_emails(mail, file, mail_message):
    current_user = get_jwt_identity()

    if not file:
        return {"message": "No file provided"}, 400

    # File Extension Validation
    file_extension = file.filename.split('.')[-1].lower()
    try:
        if file_extension == 'xlsx':
            data = pd.read_excel(file)  # Read Excel file
        elif file_extension == 'csv':
            data = pd.read_csv(file)  # Read CSV file
        else:
            return {"message": "Unsupported file format. Please upload .csv or .xlsx files"}, 400

        # CSV Column Validation
        required_columns = {'email_id', 'subject'}
        if not required_columns.issubset(data.columns):
            return jsonify({"error": f"CSV must contain the following columns: {required_columns}"}), 400

        # Check for Missing Email Addresses
        if data['email_id'].isnull().sum() > 0:
            return jsonify({"error": "Missing email addresses in the file"}), 400

        # Send Emails
        for index, row in data.iterrows():
            updated_message = mail_message

            # Replace placeholders dynamically based on additional columns
            for column_name in data.columns[2:]:
                updated_message = updated_message.replace("-----", str(row[column_name]), 1)

            # Construct the email content
            html_content = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Mozilla Firefox Club - Attendance Portal</h2>
                    <p>Dear {row.get('Name', 'Student')},</p>
                    
                    <p>{updated_message}</p>
                    
                    <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px;">
                        <h3>Login Credentials</h3>
            """
            for column_name in data.columns[2:]:
                html_content += f"<p><strong>{column_name}:</strong> {row[column_name]}</p>"

            html_content += """
                    </div>
                    
                    <p>Portal Link: <a href="https://exc-attendance.vercel.app/">EXC Attendance Portal</a></p>
                    
                    <p>Best regards,<br>Mozilla Firefox Club<br>Vellore Institute of Technology</p>
                </div>
            """

            # Create Email Message
            msg = Message(
                subject=row['subject'],
                recipients=[row['email_id']],
                sender=os.getenv('MAIL_SENDER')
            )
            msg.html = html_content
            mail.send(msg)

            # Save Email Record to Database
            email_record = EmailRecords(
                recipient=row['email_id'],
                subject=row['subject'],
                message=updated_message,
                sender=current_user["username"]
            )
            email_record.save()

        return jsonify({"message": "Emails sent successfully!"}), 200

    except Exception as e:
        return {"message": f"Error processing file: {str(e)}"}, 500

