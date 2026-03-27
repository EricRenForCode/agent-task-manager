from datetime import date
from typing import List, Dict

from pydantic import BaseModel


# ==================== Calendar Schemas ====================

class DayTaskCount(BaseModel):
    todo: int
    ongoing: int
    done: int


class MonthlyDayInfo(BaseModel):
    date: date
    has_tasks: bool
    task_count: DayTaskCount
    total_tokens: int


class MonthlyCalendarResponse(BaseModel):
    year: int
    month: int
    days: List[MonthlyDayInfo]


class DailyTaskSummary(BaseModel):
    total_tasks: int
    total_tokens: int
    agents_involved: List[str]


class DailyCalendarResponse(BaseModel):
    date: date
    tasks: Dict[str, List[dict]]  # todo, ongoing, done
    summary: DailyTaskSummary
