from datetime import datetime

# -------- VIEW --------
def clamp_pagination(skip: int,
                     limit: int) -> tuple[int, int]:
    skip = max(skip, 0)
    limit = min(max(limit, 1), 100)
    return skip, limit

# -------- FINE --------
def days_overdue(due_date: datetime,
                 returned_at: datetime) -> int:
    delta_days = (returned_at.date() - due_date.date()).days
    return max(delta_days, 0)
