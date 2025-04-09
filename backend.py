from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Get data from the request
        data = request.json
        object_name = data['object_name']
        toddler_id = data['toddler_id']
        recipient_email = data['recipient_email']

        # Gmail SMTP server configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # TLS port
        sender_email = "miniguardai1@gmail.com"  
        sender_password = "txli imgt erom ykur"  

        # Compose the email
        subject = f"🚨 ALERT: Dangerous Object Detected Near Child"
        body = f"""
        Dear Parent,

        A dangerous object ({object_name}) has been detected near your child (ID: {toddler_id}).
        Please take immediate action!

        Stay safe,
        MiniGuard AI
        """

        # Set up MIME structure for email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)  # Log in with email and App password
            server.sendmail(sender_email, recipient_email, msg.as_string())  # Send email

        return jsonify({"message": "Email sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)