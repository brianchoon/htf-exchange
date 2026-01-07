from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass(frozen=True)
class UserAction:
    timestamp: datetime
    user_id: str
    username: str
    action: str

    def __str__(self) -> str:
        ts = self.timestamp.isoformat().replace("+00:00", "Z")

        return f"{ts} | {self.user_id} | {self.username} | {self.action}"

    def to_dict(self):
        data = asdict(self)

        data["timestamp"] = self.timestamp.isoformat()
        return data
