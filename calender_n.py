import platform
import calendar
from datetime import datetime

import ttk
import tktable

LINUX = platform.system() == 'Linux'

def get_calendar(locale, fwday):
    if locale is None:
        return calendar.TextCalendar(fwday)
    else:
        return calendar.LocaleTextCalendar(fwday, locale)


class ArrowButton(ttk.Button):
    arrow_layout = lambda self, direc: (
        [('Button.focus', {'children': [('Button.%sarrow' % direc, None)]})]
        )

    def __init__(self, master, **kw):
        direction = kw.pop('direction', 'left')
        style = ttk.Style(master)

        # XXX urgh
        if LINUX:
            style.layout('L.TButton', self.arrow_layout('left'))
            style.layout('R.TButton', self.arrow_layout('right'))
            kw['style'] = 'L.TButton' if direction == 'left' else 'R.TButton'
        else:
            kw['text'] = u'\u25C0' if direction == 'left' else u'\u25B6'
            kw['style'] = 'Arrow.TButton'
            style.configure(kw['style'], width=2, padding=0)
        # urgh end

        ttk.Button.__init__(self, master, **kw)


class Calendar(ttk.Frame, object):
    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master)

        params = {'locale': None, 'titlebg': 'blue', 'titlefg': 'white',
            'calendarbg': 'white'}
        params.update(kw)
        for arg, val in params.iteritems():
            setattr(self, "_%s" % arg, val)

        date = datetime.now()
        self._year, self._month = date.year, date.month

        self._setup_style()
        self._build_topbar()

        # calendar
        self._cal = get_calendar(self._locale, calendar.SUNDAY)
        self._tclarray = tktable.ArrayVar(self)
        cols = self._cal.formatweekheader(3).split()
        self.table = tktable.Table(self, variable=self._tclarray,
            highlightthickness=4, highlightcolor=self._calendarbg,
            highlightbackground=self._calendarbg,
            cols=len(cols) + 1, rows=7, background=self._calendarbg,
            titlerows=1, titlecols=1, roworigin=-1, colorigin=-1,
            bd=0, cursor='arrow', resizeborders='none', colwidth=5,
            state='disabled', browsecommand=self._set_selection)
        self.table.pack(side='bottom')
        self.table.bind('<Map>', self._set_minsize)

        self._setup_table(cols)
        # update calendar
        self._yeardates = self._year


    def next_month(self):
        if self._month == 12:
            self._month = 1
            self._year += 1
            self._yeardates = self._year
        else:
            self._month += 1
            self._adjust_calendar(self._month)


    def prev_month(self):
        if self._month == 1:
            self._month = 12
            self._year -= 1
            self._yeardates = self._year
        else:
            self._month -= 1
            self._adjust_calendar(self._month)


    def next_year(self):
        self._year += 1
        self._yeardates = self._year


    def prev_year(self):
        self._year -= 1
        self._yeardates = self._year



    def _setup_style(self):
        style = ttk.Style(self)
        if LINUX:
            style.theme_use('clam')

    def _build_topbar(self):
        bar = ttk.Frame(self, relief='raised', padding=4)
        bar.pack(side='top', fill='x')
        lbtn = ArrowButton(bar, direction='left', command=self.prev_month)
        rbtn = ArrowButton(bar, direction='right', command=self.next_month)
        self._monthlbl = ttk.Label(bar, text=calendar.month_name[self._month],
            width=len(max(calendar.month_name)), anchor='center')
        lbtn.grid(row=0, column=0, sticky='w')
        self._monthlbl.grid(row=0, column=1, padx=6)
        rbtn.grid(row=0, column=2, sticky='w')

        spacer = ttk.Label(bar, text='')
        spacer.grid(row=0, column=3, sticky='ew')

        lbtn2 = ArrowButton(bar, direction='left', command=self.prev_year)
        rbtn2 = ArrowButton(bar, direction='right', command=self.next_year)
        self._yearlbl = ttk.Label(bar, text=self._year)
        lbtn2.grid(row=0, column=4, sticky='e')
        self._yearlbl.grid(row=0, column=5, padx=6, sticky='e')
        rbtn2.grid(row=0, column=6, sticky='e')

        bar.grid_columnconfigure(3, weight=1)

    def _setup_table(self, cols):
        table = self.table
        table.tag_configure('title', bg=self._titlebg, fg=self._titlefg)

        array = self._tclarray
        for indx, col in enumerate(cols):
            table_indx = '-1,%d' % indx
            array[table_indx] = col

    def _adjust_calendar(self, month_now):
        array = self._tclarray
        table = self.table
        month_0 = month_now - 1
        # remove the 'not_this_month' tag from items that were using it and
        # possibly won't be redisplayed now.
        table.tag_delete('not_this_month')
        table.tag_configure('not_this_month', fg='grey70')
        # XXX clear selection
        table.selection_clear('all')

        # update values in calendar
        self._monthlbl['text'] = calendar.month_name[month_now]
        for week_indx, week in enumerate(self._yeardates[month_0]):
            array['%d,-1' % week_indx] = week[0].strftime('%U')
            for day_indx, date in enumerate(week):
                table_indx = '%d,%d' % (week_indx, day_indx)
                array[table_indx] = date.day
                if date.month != month_now:
                    table.tag_cell('not_this_month', table_indx)

        # erase data in rows that weren't overrwritten
        for row in range(len(self._yeardates[month_0]), 6):
            for i in range(-1, 7):
                array.unset('%d,%d' % (row, i))

    def _set_minsize(self, event):
        self.master.wm_minsize(self.winfo_width(), self.winfo_height())

    def _get_year_dates(self):
        return self.__year_dates

    def _set_year_dates(self, year):
        self.__year_dates = [
            self._cal.monthdatescalendar(year, i)
                for i in range(calendar.January, calendar.January+12)
            ]
        self._yearlbl['text'] = year
        self._adjust_calendar(self._month)

    def _get_selected(self):
        week, day = self.__selected
        date = self._yeardates[self._month - 1][week][day]
        return (date.year, date.month, date.day)

    def _set_selection(self, event):
        if event.r == -1 or event.c == -1 or not self._tclarray.get(event.C):
            return

        self.__selected = (event.r, event.c)
        self.event_generate('<<date-selected>>')

    _yeardates = property(_get_year_dates, _set_year_dates)
    selected = property(_get_selected, _set_selection)


def sample():
    def print_date(event):
        print event.widget.selected

    cal = Calendar(titlebg='#2077ed', titlefg='white')
    cal.pack()
    cal.bind('<<date-selected>>', print_date)
    cal.mainloop()

if __name__ == "__main__":
    sample()