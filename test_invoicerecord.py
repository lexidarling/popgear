import pytest
from invoicerecord import InvoiceRecord

aprsix = {'month': 4, 'day': 6, 'year': 2019}
aprtwenty = {'month': 4, 'day': 20, 'year': 2019}

mockrec = {'part_id': 'RM32AI',
           'part_qty': 2,
           'part_rate': 5,
           'start_date': aprsix,
           'end_date': aprtwenty}


@pytest.mark.parametrize("rec,dur", [(mockrec, 3)])
def test_record_dur(rec, dur):
    assert InvoiceRecord(**rec).record_dur == dur


@pytest.mark.parametrize("rec,tot", [(mockrec, 30)])
def test_record_total(rec, tot):
    assert InvoiceRecord(**rec).record_total == tot
