import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dataclasses import dataclass


@dataclass
class EmailConfig:
    """
    📧 Configuration for email sending.

    This dataclass holds the necessary configuration for connecting to an SMTP server
    and sending emails.

    Attributes:
        smtp_server (str): The SMTP server address.
        smtp_port (int): The port number for the SMTP server.
        smtp_username (str): The username for SMTP authentication.
        smtp_password (str): The password for SMTP authentication.
        sender_email (str): The email address to be used as the sender.

    🔒 Note: Ensure that sensitive information like passwords are handled securely.
    """
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    sender_email: str


class EmailSender:
    """
    📨 Email Sending Service

    This class provides functionality to send emails using the configured SMTP server.

    🔑 Features:
    - Supports both HTML and plain text email content
    - Uses TLS for secure communication with the SMTP server
    - Provides error handling and logging for email sending attempts

    🛠️ Usage:
    Instantiate this class with an EmailConfig object, then use the send_email method
    to send emails.
    """

    def __init__(self, config: EmailConfig):
        """
        Initialize the EmailSender with the provided configuration.

        Args:
            config (EmailConfig): Configuration for the email sending service.
        """
        self.config = config

    def send_email(self, to: str, subject: str, body: str, is_html: bool = True) -> None:
        """
        📤 Send an email using the configured SMTP server.

        Args:
            to (str): The recipient's email address.
            subject (str): The subject of the email.
            body (str): The content of the email.
            is_html (bool, optional): Whether the email body is HTML. Defaults to True.

        🔔 Note:
        This method currently simulates sending an email and prints a success message.
        To actually send emails, uncomment the `server.send_message(message)` line and
        comment out the `print("simulated sending")` line.

        💡 Error Handling:
        If an error occurs during the email sending process, it will be caught and printed.
        In a production environment, consider using proper logging and error reporting.
        """
        message = MIMEMultipart()
        message["From"] = self.config.sender_email
        message["To"] = to
        message["Subject"] = subject

        content_type = "html" if is_html else "plain"
        message.attach(MIMEText(body, content_type))

        try:
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.smtp_username, self.config.smtp_password)
                # server.send_message(message)
                print("simulated sending")

            print(f"Email successfully sent to {to}")

        except Exception as e:
            print(f"Error sending email: {e}")
