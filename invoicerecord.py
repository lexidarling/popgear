from dataclasses import dataclass
from datetime import date, timedelta

@dataclass
class InvoiceRecord:

    part_id: str
    part_qty: int
    start_date: date
    due_date: date
    part_desc: str = ''
    part_rate: int = None

    @property
    def record_total(self):
        return self.part_rate * self.part_qty * self.record_dur

    @property
    def record_dur(self):
        dl = (self.due_date - self.start_date)
        dur = dl / timedelta(weeks=1)
        return int(dur + 1)
