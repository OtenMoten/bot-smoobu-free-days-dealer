import logging

import requests
from cachetools import TTLCache
from ratelimit import limits, sleep_and_retry
from typing import Dict, Any

from config import API_BASE_URL, API_KEY, CACHE_EXPIRATION, RATE_LIMIT
from exceptions import RateLimitExceeded, AuthenticationError, SmoobuAPIError
from interfaces.api_client import APIClient

logger = logging.getLogger(__name__)


class SmoobuAPIClient(APIClient):
    """
    🌐 Smoobu API Client Implementation

    This class provides a concrete implementation of the APIClient interface
    specifically for interacting with the Smoobu API. It includes features such as
    rate limiting, caching, and error handling.

    🔑 Key Features:
    - Rate limiting to comply with API usage restrictions
    - Caching of API responses to reduce unnecessary requests
    - Custom error handling for common API issues

    🛠️ Configuration:
    The client uses the following configuration parameters:
    - API_BASE_URL: The base URL for the Smoobu API
    - API_KEY: The authentication key for accessing the API
    - CACHE_EXPIRATION: The time-to-live (TTL) for cached responses
    - RATE_LIMIT: The maximum number of API calls allowed per second

    🔗 Usage:
    This client is typically used within the SmoobuService to interact with the Smoobu API,
    fetching data such as reservations and user information.
    """

    def __init__(self):
        """
        Initialize the SmoobuAPIClient.

        Sets up the base URL, headers for authentication, and initializes the cache.
        """
        self.base_url = API_BASE_URL
        self.headers = {
            "Api-Key": API_KEY,
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }
        self.cache = TTLCache(maxsize=100, ttl=CACHE_EXPIRATION)

    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=1)
    def get(self, endpoint: str) -> Dict[str, Any]:
        """
        🔍 Perform a GET request to the specified Smoobu API endpoint.

        This method implements rate limiting and caching to optimize API usage.
        It also handles various error scenarios, raising appropriate custom exceptions.

        Args:
            endpoint (str): The API endpoint to send the GET request to.

        Returns:
            Dict[str, Any]: A dictionary containing the API response data.

        Raises:
            RateLimitExceeded: If the API rate limit is exceeded.
            AuthenticationError: If there's an authentication problem.
            SmoobuAPIError: For other API-related errors.

        🔒 Rate Limiting:
        The method is decorated with @sleep_and_retry and @limits to ensure
        compliance with the API's rate limiting policy.

        💾 Caching:
        Responses are cached to reduce API calls. Cached responses are returned
        for subsequent requests to the same endpoint within the cache TTL.

        💡 Note:
        This method handles common HTTP errors and translates them into
        custom exceptions for easier error handling in the application.
        """
        if endpoint in self.cache:
            return self.cache[endpoint]

        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            self.cache[endpoint] = data
            return data
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                raise RateLimitExceeded("API rate limit exceeded") from e
            elif e.response.status_code == 401:
                raise AuthenticationError("Authentication failed") from e
            else:
                raise SmoobuAPIError(f"HTTP error occurred: {e}") from e
        except requests.exceptions.RequestException as e:
            raise SmoobuAPIError(f"An error occurred: {e}") from e

    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=1)
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a POST request to the specified Smoobu API endpoint.

        Args:
            endpoint (str): The API endpoint to send the POST request to.
            data (Dict[str, Any]): The data to be sent in the request body.

        Returns:
            Dict[str, Any]: A dictionary containing the API response data.

        Raises:
            RateLimitExceeded: If the API rate limit is exceeded.
            AuthenticationError: If there's an authentication problem.
            SmoobuAPIError: For other API-related errors.
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                raise RateLimitExceeded("API rate limit exceeded") from e
            elif e.response.status_code == 401:
                raise AuthenticationError("Authentication failed") from e
            else:
                raise SmoobuAPIError(f"HTTP error occurred: {e}") from e
        except requests.exceptions.RequestException as e:
            raise SmoobuAPIError(f"An error occurred: {e}") from e

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
        endpoint = f"reservations/{reservation_id}/messages/send-message-to-host"
        data = {
            "subject": subject,
            "messageBody": message_body,
            "internal": internal
        }
        return self.post(endpoint, data)
