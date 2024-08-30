from dataclasses import dataclass
from typing import List

from dto.base import BaseDTO


@dataclass
class ApartmentDTO(BaseDTO):
    id: int
    name: str


@dataclass
class ChannelDTO(BaseDTO):
    id: int
    name: str


@dataclass
class BookingDTO(BaseDTO):
    id: int
    reference_id: str
    guest_name: str
    email: str
    arrival: str
    departure: str
    price: float
    apartment: ApartmentDTO
    channel: ChannelDTO


@dataclass
class ReservationsDTO(BaseDTO):
    total_items: int
    bookings: List[BookingDTO]
