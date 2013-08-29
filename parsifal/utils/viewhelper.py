def _extract_attrs(attrs):
    str_attrs = ''
    if attrs:
        for key in attrs.keys():
            str_attrs += ' %s="%s"' % (key, attrs[key])
    return str_attrs

def _pretty_name(name):
    if not name:
        return ''
    return name.replace('_', ' ').capitalize()


class HtmlTable:

    def __init__(self):
        self._header = []
        self._body = []
        self._data = []
        self._id = ''
        self._class = ''
        self._attrs = {}  

    def id(self, value):
        self._id = value
        return self

    def css_class(self, value):
        self._class += ' ' + value
        return self

    def attrs(self, values):
        self._attrs = dict(self._attrs.items() + values.items())
        return self

    def header(self, *args):
        for arg in args:
            if type(arg) is list:
                for attr in arg:
                    self._header.append(attr)
            else:
                self._header.append(arg)
        return self

    def data_attrs(self, *args):
        for arg in args:
            if type(arg) is list:
                for attr in arg:
                    self._body.append(attr)
            else:
                self._body.append(arg)
        return self

    def data(self, values):
        self._data = values
        return self

    def _extract_dict_columns(self, values):
        for key in values.keys():
            self._header.append(key)
            self._body.append(values[key])

    def _extract_list_columns(self, values):
        for value in values:
            self._header.append(_pretty_name(value))
            self._body.append(value)

    def columns(self, values):
        if type(values) is dict:
            self._extract_dict_columns(values)
            pass
        elif type(values) is list:
            self._extract_list_columns(values)
        return self

    def _join_attrs(self):
        if self._id:
            self._attrs['id'] = self._id
        if self._class:
            if 'class' in self._attrs.keys():
                self._attrs['class'] = self._attrs['class'] + ' ' + self._class
            else: 
                self._attrs['class'] = self._class
        return self._attrs

    def build(self):
        html = '<table%s>' % _extract_attrs(self._join_attrs())

        if self._header:
            html += '<thead><tr>'
            for col in self._header:
                html += '<th>%s</th>' % col
            html += '</tr></thead>'

        if self._body:
            html += '<tbody>'
            for element in self._data:
                html += '<tr>'
                for col in self._body:
                    html += '<td>%s</td>' % getattr(element, col)
                html += '</tr>'
            html += '</tbody>'

        html += '</table>'

        return html