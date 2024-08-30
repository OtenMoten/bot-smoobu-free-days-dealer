class SmoobuAPIError(Exception):
    """
    🚫 Base exception class for Smoobu API errors.

    This exception serves as the parent class for all Smoobu API-related exceptions.
    It allows for catching any Smoobu API error generically while also enabling
    more specific error handling when needed.

    🛠️ Usage:
    - Catch this exception to handle any Smoobu API error generically.
    - Subclass this exception for more specific Smoobu API error types.

    Example:
    ```python
    try:
        # Some Smoobu API operation
    except SmoobuAPIError as e:
        print(f"A Smoobu API error occurred: {e}")
    ```
    """
    pass


class RateLimitExceeded(SmoobuAPIError):
    """
    ⏱️ Exception raised when the Smoobu API rate limit is exceeded.

    This exception is thrown when the application has made too many requests
    to the Smoobu API within a given time frame.

    🛠️ Usage:
    - Catch this exception to implement rate limiting logic, such as
      exponential backoff or request queuing.

    Example:
    ```python
    try:
        # Smoobu API operation
    except RateLimitExceeded:
        time.sleep(60)  # Wait for 60 seconds before retrying
        # Retry the operation
    ```
    """
    pass


class AuthenticationError(SmoobuAPIError):
    """
    🔐 Exception raised when there's an authentication problem with the Smoobu API.

    This exception is thrown when the API request fails due to invalid credentials
    or authentication tokens.

    🛠️ Usage:
    - Catch this exception to handle authentication failures, such as
      refreshing tokens or prompting for new credentials.

    Example:
    ```python
    try:
        # Smoobu API operation
    except AuthenticationError:
        refresh_auth_token()
        # Retry the operation with the new token
    ```
    """
    pass
