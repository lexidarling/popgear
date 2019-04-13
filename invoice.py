import json
from invoicerecord import InvoiceRecord
from pathlib import Path

ROWS = 66
COLS = 80

INVOICE_FILE = 'test_invoice.json'
INVENTORY_FILE = 'test_inventory.json'


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
    
    def __init__(self, inventory, invoice=None, records=None):
        self.records = records or []
        if invoice:
            for r in invoice.get('records'):
                records.append(self.make_record(r))
        self.inventory = inventory

    def make_record(self, record):
        part_info = self.inventory[record['part_id']]
        record.update(part_info)
        
        return InvoiceRecord(**record)

    def make_client(self, invoice):
        rh = [justify_left('Ship To:', COLS/2)]
        for line in invoice['shipping_info']:
            rh.append(justify_left(line, COLS/2))
        billing = invoice['billing_info']
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
        return clientinfo

    def make_header(self):
        h = [justify_centered('Rental Invoice', COLS)]
        h.append(justify_left('', COLS))
        for line in self.inventory['company_info']:
            h.append(justify_left(line, COLS))
        return h

    def make_footer(self):
        f = [justify_centered('', COLS)]
        f.append(justify_centered('popgear', COLS))
        return f

    def make_datablock(self, invoice, rows):
        recs = invoice['record']
        data_rows = rows - 7 # 2 break, 1 header, 1 total, 1 discount, 1 final
        if len(recs) > data_rows:
            raise NotImplementedError
        ttl = 0
        for r in recs:
            ttl += r.record_total()
        disc = invoice.get('discount', 0)
        final = ttl - ((disc/100) * ttl)

        db = [self.render_header()]
        db.append(make_break('-', COLS))
        for r in recs:
            db.append(self.render_rec(r))
        db.append(make_break('-', COLS))
        db.append(self.render_ttl_line('Total: ', ttl))
        db.append(self.render_ttl_line('Discount: ', disc))
        db.append(self.render_ttl_line('Final: ', final()))



    def render_ttl_line(self, title, val):
        rh = VERT_DIV
        rh += justify_right((ttl), 12)
        rh += VERT_DIV
        rh = title + t
        lh = VERT_DIV
        rem = COLS - (len(rh) + len(lh))
        line = lh + justify_center('', rem) + rh
        return line


    def render_header(self):
        lh = VERT_DIV
        lh += justify_centered('PART#', 8)
        lh += VERT_DIV
        rh += VERT_DIV
        rh += justify_centered('Start Date', 10)
        rh += VERT_DIV
        rh += justify_centered('End Date', 10)
        rh += VERT_DIV
        rh += justify_centered('Rate', 8)
        rh += VERT_DIV
        rh += justify_centered('Qty', 4)
        rh += VERT_DIV
        rh += justify_centered('Total', 8)
        rh += VERT_DIV
        rem = COLS - (len(rh) + len(lh))
        line = lh + justify_centered('Description', rem) + rh
        return line

    def render_rec(self, rec):
        lh = VERT_DIV
        lh += justify_centered(rec.part_id, 8)
        lh += VERT_DIV
        rh += VERT_DIV
        rh += justify_centered(rec.start_date, 10)
        rh += VERT_DIV
        rh += justify_centered(rec.end_date, 10)
        rh += VERT_DIV
        rh += justify_centered(rec.part_rate, 8)
        rh += VERT_DIV
        rh += justify_centered(rec.part_qty, 4)
        rh += VERT_DIV
        rh += justify_centered(rec.record_total, 8)
        rh += VERT_DIV
        rem = COLS - (len(rh) + len(lh))
        line = lh + justify_centered(rec.part_desc, rem) + rh
        return line
            
def load_invoice(fn):
    with open(fn) as f:
        invc = json.load(f)
    return invc

def load_inentory(fn):
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


def main():
    inventory = load_inventory(INVENTORY_FILE)

    invc_file = Path(INVOICE_FILE).expanduser()
    if invc_file.exists():
        invoice = load_invoice(INVOICE_FILE)
        inv = Invoice(inventory, invoice=invoice)
        
        head = inv.make_header()
        client = inv.make_client(invoice)
        foot = inv.make_footer()
        
        rem = ROWS - (len(head) + len(client) + len(foot))

        datablock = inv.make_datablock(invoice, rem)
        
        doc = head + client + datablock + foor
        for d in doc:
            print(d)


class NotTruncatingForYouError(NotImplementedError):
    pass


if __name__ == '__main__':
    main()
