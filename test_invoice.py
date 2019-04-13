import pytest
import invoice


mockin = invoice.Invoice(inventory={'RM32AI': {'part_rate': 30, 'part_desc': 'Rack mixer'},
            'SM57': {'part_rate': 5, 'part_desc': 'Shure Handheld'},
            'company_info': ['Prof Oak Prod', 'Santa Clara CA', 'prof@profoakprod.com']})

mockvoice = {'record': [{'part_id': 'RM32AI', 'part_qty': 2, 'start_date': '04/06/09', 'due_date': '04/06/09'},
                        {'part_id': 'SM57', 'part_qty': 2, 'start_date': '04/06/09', 'due_date': '04/06/09'}],
            'billing_info': ['Sunnyvale Community Playres', '500 Laurelwood'],
            'shipping_info': ['N/A Pickup']}

def test_justify_right():
    with pytest.raises(invoice.NotTruncatingForYouError):
        invoice.justify_right('hello', 2)
    assert invoice.justify_right('Prof Oak Prod', 40) == '                           Prof Oak Prod'

def test_justify_left():
    with pytest.raises(invoice.NotTruncatingForYouError):
        invoice.justify_left('hello', 2)
    assert invoice.justify_left('Prof Oak Prod', 40) == 'Prof Oak Prod                           '

def test_make_record():
    assert invoice.Invoice.make_record(mockin, {'part_id': 'RM32AI', 'part_qty': 2, 'start_date': '04/06/09', 'due_date': '04/06/09'})


def test_make_client():
    assert invoice.Invoice.make_client(mockin, mockvoice) == [\
'Bill To:                                '+'Ship To:                                ',
'Sunnyvale Community Playres             '+'N/A Pickup                              ',
'500 Laurelwood                          '+'                                        ']

def test_make_header():
    assert invoice.Invoice.make_header(mockin) == [\
'                                 Rental Invoice                                 ',
'                                                                                ',
'Prof Oak Prod                                                                   ',
'Santa Clara CA                                                                  ',
'prof@profoakprod.com                                                            ']

def test_make_footer():
    assert invoice.Invoice.make_footer(mockin) == [\
'                                                                                ',
'                                    popgear                                     ']
