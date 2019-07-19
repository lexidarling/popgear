import pytest
import invoice


mockin = invoice.Invoice(inventory={'RM32AI': {'part_rate': 30, 'part_desc': 'Rack mixer'}, # noqa
                                    'SM57': {'part_rate': 5, 'part_desc': 'Shure Handheld'}, # noqa
                                    'company_info': ['Prof Oak Prod', 'Santa Clara CA', 'prof@profoakprod.com']}) # noqa

bill = ['Sunnyvale Community Playres', '500 Laurelwood']
ship = ['N/A Pickup']

aprsix = {'month': 4, 'day': 6, 'year': 2019}
aprtwenty = {'month': 4, 'day': 20, 'year': 2019}

mockrm = {'part_id': 'RM32AI',
          'part_qty': 2,
          'start_date': aprsix,
          'end_date': aprtwenty}

mocksm = {'part_id': 'SM57',
          'part_qty': 2,
          'start_date': aprsix,
          'end_date': aprtwenty}
mockrec = {'part_id': 'RM32AI',
           'part_qty': 2,
           'part_rate': 5,
           'start_date': aprsix,
           'end_date': aprtwenty}

mockvoice = {'record': [mockrm, mocksm],
             'billing_info': bill,
             'shipping_info': ship}

# @pytest.mark.parametrize("rec,dur", [(mockrec, 3)])


def test_justify_right():
    with pytest.raises(invoice.NotTruncatingForYouError):
        invoice.justify_right('hello', 2)
    assert invoice.justify_right('Prof Oak Prod', 40) == '                           Prof Oak Prod' # noqa


def test_justify_left():
    with pytest.raises(invoice.NotTruncatingForYouError):
        invoice.justify_left('hello', 2)
    assert invoice.justify_left('Prof Oak Prod', 40) == 'Prof Oak Prod                           ' # noqa


def test_make_record():
    assert invoice.Invoice.make_record(mockin, mockrec)


def test_make_client():
    assert invoice.Invoice.make_client(mockin, mockvoice) == [
'Bill To:                                '+'Ship To:                                ', # noqa
'Sunnyvale Community Playres             '+'N/A Pickup                              ', # noqa
'500 Laurelwood                          '+'                                        ', # noqa
'                                                                                '] # noqa


def test_make_header():
    assert invoice.Invoice.make_header(mockin) == [
'                                 Rental Invoice                                 ', # noqa
'                                                                                ', # noqa
'Prof Oak Prod                                                                   ', # noqa
'Santa Clara CA                                                                  ', # noqa
'prof@profoakprod.com                                                            ', # noqa
'                                                                                '] # noqa


def test_make_footer():
    assert invoice.Invoice.make_footer(mockin) == [
'                                                                                ', # noqa
'                                    popgear                                     '] # noqa
