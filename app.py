import logging
from datetime import datetime

from exceptions import SmoobuAPIError
from interfaces.formatter import Formatter
from services.smoobu_service import SmoobuService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SmoobuApp:
    """
    🏨 Main Application for Smoobu API Interactions

    This class orchestrates the interactions with the Smoobu API, formatting the results,
    and presenting the information.

    🔑 Features:
    - Retrieves user information, reservations, and bookings
    - Uses various formatters to present the data in a readable format
    - Handles errors and provides logging

    🔗 Dependencies:
    - SmoobuService for API interactions
    - Various Formatter implementations for data presentation
    """

    def __init__(self, service: SmoobuService, reservations_formatter: Formatter,
                 user_formatter: Formatter, booking_list_formatter: Formatter,
                 unoccupied_days_formatter: Formatter):
        """
        Initialize the SmoobuApp with necessary services and formatters.

        Args:
            service (SmoobuService): Service for Smoobu API interactions.
            reservations_formatter (Formatter): Formatter for reservations data.
            user_formatter (Formatter): Formatter for user information.
            booking_list_formatter (Formatter): Formatter for booking lists.
            unoccupied_days_formatter (Formatter): Formatter for unoccupied days.
        """
        self.service = service
        self.reservations_formatter = reservations_formatter
        self.user_formatter = user_formatter
        self.booking_list_formatter = booking_list_formatter
        self.unoccupied_days_formatter = unoccupied_days_formatter

    def run(self):
        """
        📊 Execute the main application logic.

        This method:
        1. Retrieves and displays user information
        2. Fetches and displays reservations
        3. Organizes and displays bookings by apartment
        4. Analyzes and displays unoccupied days

        🚫 Error Handling:
        Catches and logs any SmoobuAPIError that occurs during execution.
        """
        logger.info("Starting Smoobu API Request Script")
        print("Smoobu API Request Script")
        print("=" * 30)
        print(f"Current Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 30)

        try:
            user_info = self.service.get_user_info()
            print(self.user_formatter.format(user_info))

            reservations = self.service.get_reservations()
            print(self.reservations_formatter.format(reservations))

            bookings_by_apartment = self.service.get_bookings_by_apartment()
            print(self.booking_list_formatter.format(bookings_by_apartment))

            print(self.unoccupied_days_formatter.format(bookings_by_apartment))

        except SmoobuAPIError as e:
            logger.error(f"An error occurred: {e}")
            print(f"An error occurred: {e}")

        logger.info("Smoobu API Request Script completed")
