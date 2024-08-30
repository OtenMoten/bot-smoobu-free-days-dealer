from dataclasses import dataclass

from dto.base import BaseDTO


@dataclass
class UserDTO(BaseDTO):
    id: int
    firstName: str
    lastName: str
    email: str

    @property
    def first_name(self):
        return self.firstName

    @property
    def last_name(self):
        return self.lastName
