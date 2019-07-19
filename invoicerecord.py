from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class InvoiceRecord:

    part_id: str
    part_qty: int
    start_date: dict
    end_date: dict
    part_desc: str = ''
    part_rate: int = None

    @property
    def record_total(self):
        return self.part_rate * self.part_qty * self.record_dur

    @property
    def record_dur(self):
        dl = (date(**self.end_date) - date(**self.start_date))
        dur = dl / timedelta(weeks=1)
        return int(dur + 1)

    @property
    def start_date_str(self):
        day = str(self.start_date['day'])
        year = str(self.start_date['year'])[2:]
        month = str(self.start_date['month'])
        return f'{month}/{day}/{year}'

    @property
    def end_date_str(self):
        day = str(self.end_date['day'])
        year = str(self.end_date['year'])[2:]
        month = str(self.end_date['month'])
        return f'{month}/{day}/{year}'
