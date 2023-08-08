from typing import Protocol, TypeVar
from flask import request

class Requestable(Protocol):
  T = TypeVar('T', bound='Requestable')

  @classmethod
  def from_request(cls: T, request: request) -> T:
    pass

  def to_db_mapping(self) -> dict:
    pass