from enum import IntEnum


class ReportStatus(IntEnum):
    """Status of the student."""

    unreturned = 0  # The student is away from school.
    returned = 1  # The student is at school.
