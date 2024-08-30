from dto.reservation import ReservationsDTO
from interfaces.formatter import Formatter


class ReservationsFormatter(Formatter):
    """
    📊 A formatter class for creating a detailed summary of reservations.

    This class implements the Formatter interface and provides a method to format
    reservation data into a structured, human-readable string output.

    🏨 The formatted output includes:
    - A summary of the reservations data (total items)
    - Detailed information for each booking

    📅 Example output:
    ```
    Reservations Summary:
    ---------------------
    Total Items: 50

    Bookings:
    -----------------------------------------
    Booking ID: 12345
    Guest: John Doe
    Apartment: Cozy Studio
    Channel: Airbnb
    Arrival: 2024-01-01
    Departure: 2024-01-05
    Total Price: €500
    -----------------------------------------
    Booking ID: 12346
    Guest: Jane Smith
    ...
    ```

    🔗 This formatter is typically used in conjunction with the SmoobuService
    and SmoobuApp to process and display reservation data retrieved from the Smoobu API.
    """

    def format(self, data: ReservationsDTO) -> str:
        """
        📝 Format the reservation data into a structured string output.

        This method takes a ReservationsDTO object containing reservation data
        and formats it into a human-readable string with a summary and detailed
        booking information.

        Args:
            data (ReservationsDTO): An object containing reservation data, including
                pagination information and a list of bookings.

        Returns:
            str: A formatted string containing the reservations summary and detailed
                 booking information.

        💡 Note: The output includes both an overall summary and individual booking details.
        """
        output = f"""
                    Reservations Summary:
                    ---------------------
                    Total Items: {data.total_items}

                    Bookings:
                    """
        for booking in data.bookings:
            output += f"""
                    -----------------------------------------
                    Booking ID: {booking.id}
                    Guest: {booking.guest_name}
                    Apartment: {booking.apartment.name}
                    Channel: {booking.channel.name}
                    Arrival: {booking.arrival}
                    Departure: {booking.departure}
                    Total Price: €{booking.price}
                    """

        return output
