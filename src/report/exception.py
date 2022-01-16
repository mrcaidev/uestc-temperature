from __future__ import annotations


class ReportException(Exception):
    """Exception in report module field."""

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.__message = message

    def __repr__(self) -> str:
        return self.__message

    def __str__(self) -> str:
        return self.__message
