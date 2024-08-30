from typing import Dict, List

from interfaces.formatter import Formatter


class BookingListFormatter(Formatter):
    """
    📋 A formatter class for creating a human-readable list of bookings grouped by apartment.

    This class implements the Formatter interface and provides a method to format
    booking data into a structured, easy-to-read string output.

    🏠 The formatted output includes:
    - A title for the booking list
    - Sections for each apartment
    - Numbered lists of bookings for each apartment, sorted by arrival date

    📅 Example output:
    ```
    Booking List by Apartment:
    ==========================

    Cozy Studio:
    ------------
    1. 2024-01-01 to 2024-01-05 (guest@example.com; John Doe)
    2. 2024-01-10 to 2024-01-15 (another@example.com; Jane Smith)

    Luxurious Suite:
    ----------------
    1. 2024-02-01 to 2024-02-07 (vip@example.com; VIP Guest)

    ```

    🔗 This formatter is typically used in conjunction with the SmoobuService
    and SmoobuApp to process and display booking data retrieved from the Smoobu API.
    """

    def format(self, data: Dict[str, List[tuple]]) -> str:
        """
        📝 Format the booking data into a structured string output.

        This method takes a dictionary of apartment names and their corresponding
        booking lists, and formats them into a human-readable string.

        Args:
            data (Dict[str, List[tuple]]): A dictionary where keys are apartment names
                and values are lists of booking tuples. Each booking tuple contains:
                (arrival_date, departure_date, email, guest_name, price)

        Returns:
            str: A formatted string containing the booking list grouped by apartment.

        💡 Note: This method sorts the bookings for each apartment by arrival date.
        """
        output = "Booking List by Apartment:\n"
        output += "==========================\n\n"

        for apartment, bookings in data.items():
            output += f"{apartment}:\n"
            output += "-" * len(apartment) + "\n"

            if bookings:
                for i, (arrival, departure, guest_email, guest_name, price) in enumerate(sorted(bookings), 1):
                    output += f"{i}. {arrival} to {departure} ({guest_email}; {guest_name}; {price})\n"
            else:
                output += "No bookings for this apartment.\n"

            output += "\n"

        return output
