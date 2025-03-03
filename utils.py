import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
logger = logging.getLogger("voice-agent")

from dotenv import load_dotenv
load_dotenv()

BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
BREVO_SENDER_PASSWORD = os.getenv("BREVO_SENDER_PASSWORD")


def save_customer_info(data: dict, filename: str = "customer_info.txt") -> bool:
    """
    Saves customer information to a file.

    Args:
        data: The customer information dictionary.
        filename: The name of the file to save to.

    Returns:
        True if the data was saved successfully, False otherwise.
    """
    try:
        with open(filename, "a") as f:
            f.write(json.dumps(data) + "\n")
        return True
    except (FileNotFoundError, IOError) as e:
        logger.error(f"Error writing to file: {e}")
        return False
    except json.JSONDecodeError as e:
        logger.error(f"Error serializing JSON data: {e}")
        return False


def format_customer_info_html(data: dict) -> str:
    """Formats customer information into HTML."""
    html_content = "<html><body><h1>Customer Info:</h1>"
    if data:
        html_content += "<ul>"
        for key, value in data.items():
            html_content += f"<li><b>{key}:</b> {value}</li>"
        html_content += "</ul>"
    else:
        html_content += "<p>No customer data provided.</p>"
    html_content += "</body></html>"
    return html_content


def send_email(
    from_email,
    to_email,
    subject,
    body,
    smtp_server="smtp-relay.brevo.com",
    smtp_port=587,
    body_type="plain",
):
    """
    Sends an email using the provided SMTP credentials.

    Args:
        from_email (str): The sender's email address.
        to_email (str): The recipient's email address.
        subject (str): The email subject.
        body (str): The email body.
        smtp_server (str, optional): The SMTP server address. Defaults to "smtp-relay.brevo.com".
        smtp_port (int, optional): The SMTP server port. Defaults to 587.
        body_type (str, optional): 'plain' or 'html'. Defaults to 'plain'.
    """

    try:
        print("send_email...")
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, body_type))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(BREVO_SENDER_EMAIL, BREVO_SENDER_PASSWORD)
            server.send_message(msg)

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")
