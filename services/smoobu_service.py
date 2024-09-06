from datetime import datetime, timedelta
from typing import Dict, List, Any

from dto.reservation import ReservationsDTO, BookingDTO, ApartmentDTO, ChannelDTO
from dto.user import UserDTO
from interfaces.api_client import APIClient


class SmoobuService:
    """
    🏨 Smoobu Service

    This class provides high-level operations for interacting with the Smoobu API,
    abstracting the complexity of API calls and data processing.

    🔑 Key Features:
    - Fetching user information
    - Retrieving and processing reservation data
    - Organizing bookings by apartment

    🔗 Dependencies:
    - Relies on an APIClient implementation for making API requests
    - Uses various DTO (Data Transfer Object) classes for structured data handling

    🛠️ Usage:
    This service is typically used by higher-level components of the application
    to retrieve and process Smoobu-related data.
    """

    def __init__(self, api_client: APIClient):
        """
        Initialize the SmoobuService.

        Args:
            api_client (APIClient): An instance of a class implementing the APIClient interface.
        """
        self.api_client = api_client

    def get_user_info(self) -> UserDTO:
        """
        👤 Fetch user information from the Smoobu API.

        Returns:
            UserDTO: A data transfer object containing user information.

        Raises:
            SmoobuAPIError: If there's an error in the API request.

        💡 Note:
        This method makes a single API call to the 'me' endpoint to retrieve
        the current user's information.
        """
        data = self.api_client.get("me")
        return UserDTO.from_dict(data)

    def get_reservations(self) -> ReservationsDTO:
        """
        📅 Fetch all reservations from the Smoobu API.

        This method handles pagination to retrieve all reservations starting
        from January 1, 2024.

        Returns:
            ReservationsDTO: A data transfer object containing all reservations.

        Raises:
            SmoobuAPIError: If there's an error in the API request.

        🔄 Pagination:
        The method automatically handles pagination, making multiple API calls
        if necessary to retrieve all reservations.

        💡 Note:
        The start date (2024-01-01) is hardcoded. Consider making this configurable
        for more flexibility.
        """
        all_bookings = []
        page = 1
        total_items = None
        page_count = None

        today = datetime.now()
        start_date = today.strftime("%Y-%m-%d")
        end_date = today + timedelta(days=21)
        end_date = end_date.strftime("%Y-%m-%d")

        while True:
            data = self.api_client.get(f"reservations?from={start_date}&to={end_date}&pageSize=100&page={page}")

            bookings = [
                BookingDTO(
                    id=b['id'],
                    reference_id=b['reference-id'],
                    guest_name=b['guest-name'],
                    email=b['email'],
                    arrival=b['arrival'],
                    departure=b['departure'],
                    price=b['price'],
                    apartment=ApartmentDTO.from_dict(b['apartment']),
                    channel=ChannelDTO.from_dict(b['channel'])
                )
                for b in data['bookings']
            ]
            all_bookings.extend(bookings)

            if total_items is None:
                total_items = data['total_items']
                page_count = data['page_count']

            if page >= page_count:
                break

            page += 1

        return ReservationsDTO(
            total_items=total_items,
            bookings=all_bookings
        )

    def get_bookings_by_apartment(self) -> Dict[str, List[tuple]]:
        """
        🏠 Organize bookings by apartment.

        This method retrieves all reservations and then organizes them into a
        dictionary where each key is an apartment name and the value is a list
        of booking tuples.

        Returns:
            Dict[str, List[tuple]]: A dictionary where keys are apartment names and
            values are lists of booking tuples. Each tuple contains:
            (arrival, departure, email, guest_name, price)

        Raises:
            SmoobuAPIError: If there's an error in fetching the reservations.

        🧹 Data Cleaning:
        This method filters out any bookings with None values in critical fields.

        💡 Note:
        This method provides a convenient way to analyze bookings on a per-apartment basis.
        """
        reservations = self.get_reservations()
        apartments = {}

        for booking in reservations.bookings:
            if booking.apartment.name not in apartments:
                apartments[booking.apartment.name] = []

            # Check if all 6 values are not None
            if all(value is not None for value in (booking.id, booking.arrival, booking.departure, booking.email, booking.guest_name, booking.price)):
                apartments[booking.apartment.name].append((booking.id, booking.arrival, booking.departure, booking.email, booking.guest_name, booking.price))

        return apartments

    def send_message_to_host(self, reservation_id: int, subject: str, message_body: str, internal: bool = False) -> Dict[str, Any]:
        """
        Send a message to the host for a specific reservation.

        Args:
            reservation_id (int): The ID of the reservation.
            subject (str): The subject of the message.
            message_body (str): The content of the message.
            internal (bool, optional): If True, the message will only be visible to the host. Defaults to False.

        Returns:
            Dict[str, Any]: A dictionary containing the API response data.

        Raises:
            SmoobuAPIError: If there's an error in sending the message.
        """
        return self.api_client.send_message_to_host(reservation_id, subject, message_body, internal)
