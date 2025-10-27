"""Domain models for the social graph."""
from dataclasses import dataclass

@dataclass(slots=True)
class User:
    """Represents a user in the social graph."""
    username: str

@dataclass(slots=True)
class Friendship:
    """Represents a bidirectional friendship between two users."""
    user1: str
    user2: str
