from dto.user import UserDTO
from interfaces.formatter import Formatter


class UserInfoFormatter(Formatter):
    """
    👤 A simple formatter class for presenting user information.

    This class implements the Formatter interface and provides a method to format
    user data into a concise, human-readable string output.

    🎨 Features:
    - Clean, easy-to-read formatting of user details
    - Consistent presentation of user information

    🔗 This formatter is typically used in conjunction with the SmoobuService
    and SmoobuApp to process and display user data retrieved from the Smoobu API.
    """

    def format(self, data: UserDTO) -> str:
        """
        📝 Format the user data into a structured string output.

        This method takes a UserDTO object containing user information
        and formats it into a human-readable string with key user details.

        Args:
            data (UserDTO): An object containing user data, including
                id, first name, last name, and email.

        Returns:
            str: A formatted string containing the user's information.

        📋 Example output:
        ```
        User Information:
        -----------------
        ID: 12345
        Name: John Doe
        Email: john.doe@example.com
        ```

        💡 Note: The output is designed to be clear and concise, focusing on
        the most important user details.
        """
        return f"""
                User Information:
                -----------------
                ID: {data.id}
                Name: {data.firstName} {data.lastName}
                Email: {data.email}
                """
