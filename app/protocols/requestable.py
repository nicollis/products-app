from typing import Protocol, TypeVar
from flask import request

class Requestable(Protocol):
  T = TypeVar('T', bound='Requestable')
  
  @classmethod
  def from_request(cls: T, request: dict) -> T:
    """
    Creates an instance of the class from a dictionary representing an HTTP request.

    Args:
        cls (type): The class to create an instance of.
        request (dict): A dictionary representing an HTTP request.

    Returns:
        T: An instance of the class.
    """
    pass

  def to_db_mapping(self) -> dict:
    pass