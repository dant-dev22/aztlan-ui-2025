import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "torneoaztlan@gmail.com"
PASSWORD = "oeih lscc qooe yukb"


def send_email(aztlan_id: str, to_email: str):
    """Envía un correo de bienvenida con el Aztlán ID al usuario."""
    subject = "Bienvenido al torneo Aztlán"
    body = (
        f"¡Felicidades! Este es tu Aztlán ID: {aztlan_id}\n\n"
        "Úsalo para terminar tu registro en el torneo.\n\n"
        "¡Nos vemos en la competencia!"
    )

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to_email, msg.as_string())
        server.quit()

        print(f"✅ Correo enviado a {to_email} con Aztlán ID {aztlan_id}")
    except Exception as e:
        print(f"❌ Error al enviar correo a {to_email}: {e}")