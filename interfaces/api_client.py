from abc import ABC, abstractmethod
from typing import Dict, Any


class APIClient(ABC):
    """
    🌐 Abstract base class for API clients.

    The APIClient class serves as a blueprint for creating specific API client
    implementations within the application. It defines a common interface that
    all concrete API client classes must implement.

    🔑 Key Concepts:
    - Abstraction: This class cannot be instantiated directly.
    - Polymorphism: Different API client implementations can be used interchangeably.

    🛠️ Use Cases:
    - Creating clients for different APIs (e.g., Smoobu API, third-party APIs).
    - Ensuring consistency across various API interactions in the application.
    - Facilitating easy addition of new API integrations or endpoints.

    🔗 In the context of the Smoobu application:
    This abstract class is the foundation for API clients like SmoobuAPIClient,
    ensuring they all adhere to a common interface for making GET and POST requests,
    as well as specific operations like sending messages to hosts.
    """

    @abstractmethod
    def get(self, endpoint: str) -> Dict[str, Any]:
        """
        🔍 Abstract method to perform a GET request to a specified API endpoint.

        Args:
            endpoint (str): The API endpoint to send the GET request to.

        Returns:
            Dict[str, Any]: A dictionary containing the API response data.

        Raises:
            NotImplementedError: If the method is not implemented in a concrete subclass.
            SmoobuAPIError: If there's an error in the API request (in implementations).
        """
        pass

    @abstractmethod
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        📤 Abstract method to perform a POST request to a specified API endpoint.

        Args:
            endpoint (str): The API endpoint to send the POST request to.
            data (Dict[str, Any]): The data to be sent in the request body.

        Returns:
            Dict[str, Any]: A dictionary containing the API response data.

        Raises:
            NotImplementedError: If the method is not implemented in a concrete subclass.
            SmoobuAPIError: If there's an error in the API request (in implementations).
        """
        pass

    @abstractmethod
    def send_message_to_host(self, reservation_id: int, subject: str, message_body: str, internal: bool = False) -> Dict[str, Any]:
        """
        💬 Abstract method to send a message to the host for a specific reservation.

        Args:
            reservation_id (int): The ID of the reservation.
            subject (str): The subject of the message.
            message_body (str): The content of the message.
            internal (bool, optional): If True, the message will only be visible to the host. Defaults to False.

        Returns:
            Dict[str, Any]: A dictionary containing the API response data.

        Raises:
            NotImplementedError: If the method is not implemented in a concrete subclass.
            SmoobuAPIError: If there's an error in sending the message (in implementations).
        """
        pass
