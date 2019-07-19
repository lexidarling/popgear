import json
import sys
from distutils.util import strtobool
from invoicerecord import InvoiceRecord
from pathlib import Path

ROWS = 66
COLS = 80

INVOICE_FILE = 'simple-invoice.json'
INVENTORY_FILE = 'test_inventory.json'

VERT_DIV = '|'

'''       title
company line
company line
companu line

billing line     ship line
billing line     ship line
billing line     ship line

header line header line header
record line record line
record line record line
record line record line
record line record line
record line record line

                        totals
                        discounts
            footnote
'''


class Invoice:

    def __init__(self, inventory, raw_invoice=None, records=None):
        self.inventory = inventory
        self.records = records or []
        self.raw_invoice = raw_invoice
        if self.raw_invoice:
            for r in self.raw_invoice.get('record'):
                self.records.append(self.make_record(r))

    def make_record(self, record):
        part_info = self.inventory[record['part_id']]
        record.update(part_info)

        return InvoiceRecord(**record)

    def make_client(self, raw_invoice):
        rh = [justify_left('Ship To:', COLS/2)]
        for line in raw_invoice['shipping_info']:
            rh.append(justify_left(line, COLS/2))
        billing = raw_invoice['billing_info']
        lh = [justify_left('Bill To:', COLS/2)]
        for line in billing:
            lh.append(justify_left(line, COLS/2))
        ld = len(rh) - len(lh)
        if ld > 0:
            for i in range(ld):
                lh.append(justify_left('', COLS/2))
        elif ld < 0:
            for i in range(abs(ld)):
                rh.append(justify_right('', COLS/2))

        clientinfo = zip(lh, rh)
        clientinfo = [''.join(x) for x in clientinfo]
        clientinfo.append(justify_left('', COLS))
        return clientinfo

    def make_header(self):
        h = [justify_centered('Rental Invoice', COLS)]
        h.append(justify_left('', COLS))
        for line in self.inventory['company_info']:
            h.append(justify_left(line, COLS))
        h.append(justify_left('', COLS))
        return h

    def make_footer(self):
        f = [justify_centered('', COLS)]
        f.append(justify_centered('popgear', COLS))
        return f

    def make_datablock(self, invoice, rows):
        recs = invoice.records
        raw_invoice = invoice.raw_invoice
        data_rows = rows - 7  # 2 break, 1 header, 1 total, 1 discount, 1 final
        if len(recs) > data_rows:
            raise NotImplementedError
        total = 0
        for r in recs:
            total += r.record_total
        disc = raw_invoice.get('discount', 0)
        final = total - ((disc/100) * total)

        db = [self.render_header()]
        db.append(make_break('-', COLS))
        for r in recs:
            db.append(self.render_rec(r))
        db.append(make_break('-', COLS))
        db.append(self.render_ttl_line('Total:', total))
        db.append(self.render_ttl_line('Discount:', disc))
        db.append(self.render_ttl_line('Final:', final))
        return db

    def render_ttl_line(self, title, val):
        rh = VERT_DIV
        rh += justify_right(title, 14)
        rh += justify_right(val, 8)
        rh += VERT_DIV
        lh = VERT_DIV
        rem = COLS - (len(rh) + len(lh))
        line = lh + make_break(' ', rem) + rh
        return line

    def render_header(self):
        lh = VERT_DIV
        lh += justify_centered('PART#', 8)
        lh += VERT_DIV
        rh = VERT_DIV
        rh += justify_centered('Srt Date', 8)
        rh += VERT_DIV
        rh += justify_centered('End Date', 8)
        rh += VERT_DIV
        rh += justify_centered('Rate', 8)
        rh += VERT_DIV
        rh += justify_centered('Qty', 4)
        rh += VERT_DIV
        rh += justify_centered('Total', 10)
        rh += VERT_DIV
        rem = COLS - (len(rh) + len(lh))
        line = lh + justify_centered('Description', rem) + rh
        return line

    def render_rec(self, rec):
        lh = VERT_DIV
        lh += justify_centered(rec.part_id, 8)
        lh += VERT_DIV
        rh = VERT_DIV
        rh += justify_centered(rec.start_date_str, 8)
        rh += VERT_DIV
        rh += justify_centered(rec.end_date_str, 8)
        rh += VERT_DIV
        rh += justify_right(f'{rec.part_rate}.00', 8)
        rh += VERT_DIV
        rh += justify_centered(rec.part_qty, 4)
        rh += VERT_DIV
        rh += justify_right(f'{rec.record_total}.00', 10)
        rh += VERT_DIV
        rem = COLS - (len(rh) + len(lh))
        line = lh + justify_left(rec.part_desc[0:rem], rem) + rh
        return line


def load_invoice(fn):
    with open(fn) as f:
        invc = json.load(f)
    return invc


def load_inventory(fn):
    with open(fn) as f:
        invt = json.load(f)
    return invt


def make_break(pat, rep):
    return pat * rep


def justify_centered(text, width):
    text = str(text)
    if len(text) > width:
        raise NotTruncatingForYouError
    pad = (width - len(text)) / 2
    s = ' ' * int(pad)
    if len(text) % 2:
        text += ' '
    s = s + text + s
    return s


def justify_right(text, width):
    text = str(text)
    if len(text) > width:
        raise NotTruncatingForYouError
    pad = width - len(text)
    s = ' ' * int(pad)
    s += text
    return s


def justify_left(text, width):
    text = str(text)
    if len(text) > width:
        raise NotTruncatingForYouError
    pad = width - len(text)
    s = text
    s += ' ' * int(pad)
    return s


def get_lines(key, text=None):
    lines = dict({key:  []})
    text = text or f'Enter {key} line ? Y/N '
    while strtobool(input(text) or 'n'):
        lines[key].append(input('Enter line: '))
    return lines


def get_dates():
    sd = int(input(f'Start day: '))
    sm = int(input(f'Start month: '))
    sy = int(input(f'Start year: '))
    ed = int(input(f'End day: '))
    em = int(input(f'End month ({sm}): ') or sm)
    ey = int(input(f'End year ({sy}): ') or sy)
    start = {'day': sd, 'month': sm, 'year': sy}
    end = {'day': ed, 'month': em, 'year': ey}
    return start, end


def main():
    if len(sys.argv) > 1:
        invc_file = Path(sys.argv[1]).expanduser()
        print(f'Invoice file: {invc_file}')
    else:
        invc_file = Path(INVOICE_FILE).expanduser()
    if len(sys.argv) > 2:
        inventory = load_inventory(sys.argv[2])
        print(f'Inventory file: {sys.argv[2]}')
    else:
        inventory = load_inventory(INVENTORY_FILE)

    if invc_file.exists():
        invoice = load_invoice(invc_file)
        inv = Invoice(inventory, raw_invoice=invoice)

        head = inv.make_header()
        client = inv.make_client(invoice)
        foot = inv.make_footer() or ['']

        rem = ROWS - (len(head) + len(client) + len(foot))

        datablock = inv.make_datablock(inv, rem)

        doc = head + client + datablock + foot
        for d in doc:
            print(d)
    else:
        # Now begins the ugly, the necessary, the code that built the first invoice
        if not strtobool(input(f'No invoice exists, create? Y/N ')):
            print('Bye')
            exit(1)
        invoice_dict = {}
        invoice_dict.update(get_lines('billing_info'))
        invoice_dict.update(get_lines('shipping_info'))
        master_start = None
        master_end = None
        if strtobool(input('Use master start and end (recommended)  Y/n ') or 'Y'):
            master_start, master_end = get_dates()
        invoice_dict['record'] = []
        while strtobool(input('Enter record line? Y/n ') or 'Y'):
            part_num = input('Enter partnum: ')
            part_qty = int(input('Enter partqty (1): ') or 1)
            if not master_start and master_end:
                start, end = get_dates()
            else:
                start = master_start
                end = master_end
            invoice_dict['record'].append({'part_id': part_num,
                                           'part_qty': part_qty,
                                           'start_date': start,
                                           'end_date': end})

        print(json.dumps(invoice_dict))
        if strtobool(input('Writeout? Y/n') or 'Y'):
            fn = invc_file
            with open(fn, 'w') as f:
                json.dump(invoice_dict, f)


class NotTruncatingForYouError(NotImplementedError):
    pass


if __name__ == '__main__':
    main()
