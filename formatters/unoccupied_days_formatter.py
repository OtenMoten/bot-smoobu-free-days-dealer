from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
from typing import Dict, List, Optional

from dto.util import DateRange, Event, ColorScheme
from interfaces.formatter import Formatter
from services.email_sender import EmailSender


class UnoccupiedDaysFormatter(Formatter):
    """
    🏨 A sophisticated formatter class for analyzing and presenting unoccupied days in apartment bookings.

    This class implements the Formatter interface and provides methods to:
    - Analyze booking data for unoccupied periods
    - Format the analysis results into a colorful, human-readable string output
    - Generate and send personalized email offers to guests

    🎨 Features:
    - Color-coded output for easy visual parsing
    - Identification of arrival and departure events
    - Calculation of free days before arrivals and after departures
    - Dynamic pricing suggestions for unoccupied periods
    - Automated email generation for personalized guest offers

    📅 The formatter focuses on a specific date range:
    - The week after next week (starting from the current date)

    🔗 This formatter works in conjunction with the SmoobuService and SmoobuApp
    to process booking data retrieved from the Smoobu API and generate actionable insights.
    """

    def __init__(self, email_sender: EmailSender, email_template_dir: str):
        """
        Initialize the UnoccupiedDaysFormatter.

        Args:
            email_sender (EmailSender): An instance of EmailSender for sending offer emails.
            email_template_dir (str): The directory containing email templates.
        """
        self.email_sender = email_sender
        self.env = Environment(loader=FileSystemLoader(email_template_dir))
        self.email_template = self.env.get_template('email_template.html')

    def format(self, data: Dict[str, List[tuple]]) -> str:
        """
        📊 Format the booking data into a structured string output and send offer emails.

        This method analyzes the booking data for each apartment, generates a formatted
        summary of unoccupied days, and sends personalized offer emails to guests.

        Args:
            data (Dict[str, List[tuple]]): A dictionary where keys are apartment names
                and values are lists of booking tuples. Each booking tuple contains:
                (arrival_date, departure_date, guest_email, guest_name, price)

        Returns:
            str: A formatted string containing the analysis of unoccupied days for all apartments.

        💡 Note: This method also triggers the sending of offer emails to guests.
        """

        today = datetime.now().date()
        date_range = self._get_next_next_week_range(today)

        formatted_output = "\n\n".join(
            self._format_apartment(apartment, date_range, self._analyze_bookings(bookings, date_range))
            for apartment, bookings in data.items()
        )

        # Send emails for each apartment
        for apartment, bookings in data.items():
            events = self._analyze_bookings(bookings, date_range)
            self._send_emails_for_apartment(apartment, events)

        return formatted_output

    @staticmethod
    def _get_next_next_week_range(today: datetime.date) -> DateRange:
        """
          📆 Calculate the date range for the week after next week.

          Args:
              today (datetime.date): The current date.

          Returns:
              DateRange: A DateRange object with start and end dates for the target week.
          """

        start = today + timedelta(days=(14 - today.weekday()))

        return DateRange(
            start=datetime.combine(start, datetime.min.time()),
            end=datetime.combine(start + timedelta(days=6), datetime.min.time())
        )

    def _analyze_bookings(self, bookings: List[tuple], date_range: DateRange) -> List[Event]:
        """
        🔍 Analyze bookings to identify arrival and departure events within the specified date range.

        Args:
            bookings (List[tuple]): List of booking tuples.
            date_range (DateRange): The target date range for analysis.

        Returns:
            List[Event]: A list of Event objects representing arrivals and departures.
        """

        occupied_days = self._create_occupied_days_dict(bookings)

        return sorted(
            (
                Event(
                    date=current_day,
                    type=occupied_days[current_day.date()]['type'],
                    guest_name=occupied_days[current_day.date()]['guest_name'],
                    guest_email=occupied_days[current_day.date()]['guest_email'],
                    free_days=self._check_free_days(occupied_days, current_day.date(), occupied_days[current_day.date()]['type']),
                    price=occupied_days[current_day.date()]['price'],
                    offer_price=self._calculate_offer_price(occupied_days[current_day.date()]['price'], occupied_days[current_day.date()]['type'])
                )
                for current_day in (date_range.start + timedelta(days=i) for i in range((date_range.end - date_range.start).days + 1))
                if current_day.date() in occupied_days and occupied_days[current_day.date()]['type'] in ['arrival', 'departure']
            ),
            key=lambda e: e.date
        )

    @staticmethod
    def _create_occupied_days_dict(bookings: List[tuple]) -> Dict[datetime.date, Dict]:
        """
           🗓️ Create a dictionary of occupied days from booking data.

           Args:
               bookings (List[tuple]): List of booking tuples.

           Returns:
               Dict[datetime.date, Dict]: A dictionary with dates as keys and booking details as values.
           """

        occupied_days = {}

        for arrival, departure, guest_email, guest_name, price in bookings:

            arrival, departure = map(lambda x: datetime.strptime(x, "%Y-%m-%d").date(), (arrival, departure))

            for current in (arrival + timedelta(days=i) for i in range((departure - arrival).days + 1)):
                occupied_days[current] = {
                    'type': 'arrival' if current == arrival else 'departure' if current == departure else 'occupied',
                    'guest_name': guest_name,
                    'guest_email': guest_email,
                    'price': float(price) / ((departure - arrival).days + 1)  # Average daily price
                }

        return occupied_days

    @staticmethod
    def _check_free_days(occupied_days: Dict[datetime.date, Dict], current_day: datetime.date, event_type: str) -> int:
        """
         🆓 Check the number of free days before an arrival or after a departure.

         Args:
             occupied_days (Dict[datetime.date, Dict]): Dictionary of occupied days.
             current_day (datetime.date): The day to check from.
             event_type (str): Either 'arrival' or 'departure'.

         Returns:
             int: The number of free days (0, 1, or 2).
         """

        days_to_check = [current_day - timedelta(days=i) for i in [1, 2]] if event_type == 'arrival' else [current_day + timedelta(days=i) for i in [1, 2]]

        return sum(1 for day in days_to_check if day not in occupied_days)

    @staticmethod
    def _calculate_offer_price(original_price: float, event_type: str) -> float:
        """
         💰 Calculate a discounted offer price for unoccupied days.

         Args:
             original_price (float): The original daily price.
             event_type (str): Either 'arrival' or 'departure' (not used in current implementation).

         Returns:
             float: The calculated offer price.
         """

        discount = 0.57  # 43% discount for both arrival and departure

        return round(original_price * discount, 2)

    def _format_apartment(self, apartment: str, date_range: DateRange, events: List[Event]) -> str:
        """
         🏠 Format the analysis results for a single apartment.

         Args:
             apartment (str): The name of the apartment.
             date_range (DateRange): The analyzed date range.
             events (List[Event]): List of arrival and departure events.

         Returns:
             str: A formatted string with color-coded event information.
         """

        header = f"{ColorScheme.BLUE}📅 Arrivals and Departures for {apartment} from {date_range.start.date()} to {date_range.end.date()}:{ColorScheme.RESET}"

        if not events:
            return f"{header}\n{ColorScheme.CYAN}No events in this period{ColorScheme.RESET}"

        event_strings = []

        for event in events:
            icon, color, days_text = ("🏡️", ColorScheme.GREEN, "before arrival") if event.type == 'arrival' else ("🧼", ColorScheme.GREEN, "after departure")
            event_strings.append(
                f"{color}{icon} {event.type.capitalize()} on {event.date.date():%Y-%m-%d}:{ColorScheme.RESET}\n"
                f"{ColorScheme.CYAN}    👤 Guest: {event.guest_name}\n"
                f"    📧 {event.guest_email}{ColorScheme.RESET}\n"
                f"{self._get_color_for_days(event.free_days)}    ⏱ {event.free_days} day{'s' if event.free_days != 1 else ''} free {days_text}{ColorScheme.RESET}\n"
                f"{ColorScheme.YELLOW}    💰 Original price: €{event.price:.2f}/day\n"
                f"    🏷️ Offer price: €{event.offer_price:.2f}/day{ColorScheme.RESET}"
            )

        return f"{header}\n" + "\n\n".join(event_strings)

    @staticmethod
    def _get_color_for_days(free_days: int) -> str:
        """
        🎨 Get the appropriate color code based on the number of free days.

        Args:
            free_days (int): The number of free days.

        Returns:
            str: A color code from the ColorScheme.
        """

        return {
            2: ColorScheme.GREEN,
            1: ColorScheme.YELLOW
        }.get(free_days, ColorScheme.RED)

    def _send_emails_for_apartment(self, apartment: str, events: List[Event]) -> None:
        """
         📧 Send offer emails to guests for a specific apartment.

         Args:
             apartment (str): The name of the apartment.
             events (List[Event]): List of arrival and departure events.
         """

        guests = {}

        for event in events:

            if event.guest_email not in guests:
                guests[event.guest_email] = {'name': event.guest_name, 'events': []}

            guests[event.guest_email]['events'].append(event)

        for guest_email, guest_data in guests.items():
            self._send_email(apartment, guest_data['name'], guest_data['events'])

    def _send_email(self, apartment: str, guest_name: str, events: List[Event]) -> None:
        """
         📤 Send a personalized offer email to a guest.

         Args:
             apartment (str): The name of the apartment.
             guest_name (str): The name of the guest.
             events (List[Event]): List of events (arrivals/departures) for this guest.
        """

        arrival_event = next((event for event in events if event.type == 'arrival'), None)
        departure_event = next((event for event in events if event.type == 'departure'), None)

        if arrival_event or departure_event:
            subject = f"Exklusives Angebot für Ihren Aufenthalt in {apartment}"

            body = self._generate_email_body(apartment, guest_name, arrival_event, departure_event)

            self.email_sender.send_email(events[0].guest_email, subject, body, is_html=True)

    def _generate_email_body(self, apartment: str, guest_name: str, arrival_event: Optional[Event], departure_event: Optional[Event]) -> str:
        """
         ✍️ Generate the HTML body for the offer email using a template.

         Args:
             apartment (str): The name of the apartment.
             guest_name (str): The name of the guest.
             arrival_event (Optional[Event]): The arrival event, if any.
             departure_event (Optional[Event]): The departure event, if any.

         Returns:
             str: The generated HTML email body.
         """

        template_data = {
            'guest_name': guest_name,
            'apartment': apartment,
            'arrival_event': arrival_event,
            'departure_event': departure_event,
        }

        return self.email_template.render(template_data)
