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
    ensuring they all adhere to a common interface for making GET requests.
    """

    @abstractmethod
    def get(self, endpoint: str) -> Dict[str, Any]:
        """
        🔍 Abstract method to perform a GET request to a specified API endpoint.

        This method must be implemented by all concrete API client classes.
        It takes an endpoint string and returns the API response as a dictionary.

        Args:
            endpoint (str): The API endpoint to send the GET request to.

        Returns:
            Dict[str, Any]: A dictionary containing the API response data.

        Raises:
            NotImplementedError: If the method is not implemented in a concrete subclass.
            SmoobuAPIError: If there's an error in the API request (in implementations).

        Example implementation in a subclass:
        ```python
        def get(self, endpoint: str) -> Dict[str, Any]:
            response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        ```

        💡 Note: Concrete implementations should handle authentication, error checking,
        and any necessary data preprocessing or postprocessing.
        """
        pass
