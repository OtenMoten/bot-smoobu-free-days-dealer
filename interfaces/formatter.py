from abc import ABC, abstractmethod
from typing import Any


class Formatter(ABC):
    """
    🎨 Abstract base class for data formatters.

    The Formatter class serves as a blueprint for creating various data formatting classes
    within the application. It defines a common interface that all concrete formatter
    classes must implement.

    🔑 Key Concepts:
    - Abstraction: This class cannot be instantiated directly.
    - Polymorphism: Different formatter implementations can be used interchangeably.

    🛠️ Use Cases:
    - Creating formatters for different data types (e.g., user info, reservations, bookings).
    - Ensuring consistency across various formatting operations in the application.
    - Facilitating easy addition of new formatting styles or data types.

    🔗 In the context of the Smoobu application:
    This abstract class is the foundation for formatters like UserInfoFormatter,
    ReservationsFormatter, and UnoccupiedDaysFormatter, ensuring they all adhere
    to a common interface.
    """

    @abstractmethod
    def format(self, data: Any) -> str:
        """
        📝 Abstract method to format data into a string representation.

        This method must be implemented by all concrete formatter classes.
        It takes input data of any type and returns a formatted string.

        Args:
            data (Any): The data to be formatted. The type can vary depending
                        on the specific formatter implementation.

        Returns:
            str: A formatted string representation of the input data.

        Raises:
            NotImplementedError: If the method is not implemented in a concrete subclass.

        Example implementation in a subclass:
        ```python
        def format(self, data: UserDTO) -> str:
            return f"User: {data.firstName} {data.lastName}, Email: {data.email}"
        ```

        💡 Note: The specific formatting logic will depend on the type of data
        being formatted and the desired output format.
        """
        pass
