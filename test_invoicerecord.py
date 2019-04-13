import pytest
from invoicerecord import InvoiceRecord
from datetime import date

def test_record_dur():
    assert InvoiceRecord(**{'part_id': 'RM32AI', 'part_qty': 2, 'start_date': date(2009,4,6), 'due_date': date(2009,4,6)})
    assert InvoiceRecord(**{'part_id': 'RM32AI', 'part_rate': 5.95, 'part_qty': 2, 'start_date': date(2009,4,6), 'due_date': date(2009,4,8)}).record_dur == 1
    assert InvoiceRecord(**{'part_id': 'RM32AI', 'part_rate': 5.95, 'part_qty': 2, 'start_date': date(2009,4,6), 'due_date': date(2009,4,20)}).record_dur == 3


def test_record_total():
    assert InvoiceRecord(**{'part_id': 'RM32AI', 'part_rate': 5, 'part_qty': 2, 'start_date': date(2009,4,6), 'due_date': date(2009,4,20)}).record_total == 30
