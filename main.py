# Developed by Team BitFuture
# Website: www.team-bitfuture.de | Email: info@team-bitfuture.de
# Lead Developer: Ossenbrück
# Website: ossenbrück.de | Email: hi@ossenbrück.de

from app import SmoobuApp
from config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL
from formatters.booking_list_formatter import BookingListFormatter
from formatters.reservations_formatter import ReservationsFormatter
from formatters.unoccupied_days_formatter import UnoccupiedDaysFormatter, EmailSender
from formatters.user_formatter import UserInfoFormatter
from services.api_client import SmoobuAPIClient
from services.email_sender import EmailConfig
from services.smoobu_service import SmoobuService


def main():
    """
    🚀 Main entry point for the Smoobu API interaction application.

    This function:
    1. Sets up the API client and service
    2. Configures the email sender
    3. Initializes all necessary formatters
    4. Creates and runs the SmoobuApp

    💡 Note:
    - Ensure all necessary environment variables are set before running.
    - The email configuration is hardcoded here. Consider moving this to a config file or environment variables.
    """
    # Initialize API client and service
    api_client = SmoobuAPIClient()
    service = SmoobuService(api_client)

    # Create and configure email sender
    email_sender = EmailSender(EmailConfig(
        smtp_server=SMTP_SERVER,
        smtp_port=SMTP_PORT,
        smtp_username=SMTP_USERNAME,
        smtp_password=SMTP_PASSWORD,
        sender_email=SENDER_EMAIL
    ))

    # Initialize and run the app
    app = SmoobuApp(
        service,
        ReservationsFormatter(),
        UserInfoFormatter(),
        BookingListFormatter(),
        UnoccupiedDaysFormatter(email_sender, "email_templates")
    )
    app.run()


if __name__ == "__main__":
    main()

# 🔒 Security Note:
# The email configuration, especially the SMTP password, should not be hardcoded in the script.
# Consider using environment variables or a secure configuration management system for sensitive data.
