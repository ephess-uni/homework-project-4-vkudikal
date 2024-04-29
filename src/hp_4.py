# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""

    ds_new = [datetime.strptime(old_, "%Y-%m-%d").strftime('%d %b %Y') for old_ in old_dates]
    return ds_new


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        raise TypeError()

    return_outpt = []

    dw = datetime.strptime(start, '%Y-%m-%d')

    for i in range(n):
        return_outpt.append(dw + timedelta(days=i))

    return return_outpt


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""

    sc = date_range(start_date, len(values))
    t = list(zip(sc, values))
    return t


def UtilityMethod(infile):
    headSet = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
               split(','))

    with open(infile, 'r') as f:
        removehdr = DictReader(f, fieldnames=headSet)
        allrestrows = [row for row in removehdr]

        allrestrows.pop(0)

    return allrestrows


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""

    frmt = '%m/%d/%Y'
    rows = UtilityMethod(infile)
    fees_ = defaultdict(float)

    for single_each_line in rows:
        patron = single_each_line['patron_id']
        duedate = datetime.strptime(single_each_line['date_due'], frmt)
        returnedDate = datetime.strptime(single_each_line['date_returned'], frmt)
        ds = (returnedDate - duedate).days
        fees_[patron] += 0.25 * ds if ds > 0 else 0.0

    final_out = [
        {'patron_id': pn, 'late_fees': f'{fs:0.2f}'} for pn, fs in fees_.items()
    ]

    with open(outfile, 'w') as wrt:
        dcrr = DictWriter(wrt, ['patron_id', 'late_fees'])
        dcrr.writeheader()
        dcrr.writerows(final_out)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':

    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())