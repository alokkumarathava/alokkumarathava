from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

app = Flask(__name__)

def send_email(name, email, image_path):
    # SMTP server configuration
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    sender_email = 'PhotoRobot@GlobalDWS.com'
    sender_password = 'Run89778'


    # Email subject and body
    subject = "Photo from the Blockchain Futurist Conference"
    body = f"""
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td align="left" valign="top">
                    <p>Hi {name},</p>
                    <p>Attached is a photo from the Blockchain Futurist Conference.</p>
                    <p>Best Regards,</p>
                    <p>Powered by <a href="https://www.globaldws.com">GlobalDWS</a></p>
                </td>
            </tr>
        </table>
    """

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'html'))

    # Open the image file and attach it to the email
    with open(image_path, 'rb') as attachment:
        mime_base = MIMEBase('application', 'octet-stream')
        mime_base.set_payload(attachment.read())
        encoders.encode_base64(mime_base)
        mime_base.add_header('Content-Disposition', f'attachment; filename={os.path.basename(image_path)}')
        msg.attach(mime_base)

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
            print(f"Email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


@app.route('/send-email', methods=['POST'])
def send_email_route():
    name = request.form.get('name')
    email = request.form.get('email')
    file = request.files.get('image_path')

    if not name or not email or not file:
        return jsonify({"error": "Missing name, email, or image file"}), 400

    # Ensure the images directory exists
    image_dir = os.path.join(os.getcwd(), 'images')
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # Save the file to the images directory
    image_path = os.path.join(image_dir, file.filename)
    file.save(image_path)
    
    # Send the email
    send_email(name, email, image_path)

    # Optionally, remove the file after sending the email
    os.remove(image_path)

    return jsonify({"status": "Email sent successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
