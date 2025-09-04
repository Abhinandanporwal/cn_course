import smtplib
from email.mime.text import MIMEText

def smtp_client():
    smtp_server = "sandbox.smtp.mailtrap.io"
    port = 587
    sender = "from@example.com"
    recipient = "to@example.com"
    
    username = "521d2beb858f86"
    password = "2f6a427b3a9d1a"

    try:
        msg = MIMEText("Hello! This is a test email sent using Python + Mailtrap SMTP.")
        msg["Subject"] = "SMTP Test"
        msg["From"] = sender
        msg["To"] = recipient

        print("Connecting to Mailtrap SMTP server...")
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(username, password)
        print("Login successful!")

        server.sendmail(sender, recipient, msg.as_string())
        print("Email sent successfully (check Mailtrap inbox)!")
        server.quit()

    except Exception as e:
        print("SMTP Error:", e)

if __name__ == "__main__":
    smtp_client()

