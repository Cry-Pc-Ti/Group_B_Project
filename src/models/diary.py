from datetime import date, datetime


class Diary:
    def __init__(
        self,
        id: int,
        user_id: int,
        date: date,
        icon: str,
        content: str,
        sleep_start: datetime,
        sleep_end: datetime,
        create_at: datetime,
    ):
        self.id = id
        self.user_id = user_id
        self.date = date
        self.icon = icon
        self.content = content
        self.sleep_start = sleep_start
        self.sleep_end = sleep_end
        self.create_at = create_at
