def _get_config(config):
    str_config = ''
    for key in config.keys():
        str_config += ' %s="%s"' % (key, config[key])
    return str_config

def _html_table(header, body, elements, configs):
    html = '<table%s><thead><tr>' % _get_config(configs)
    for col in header:
        html += '<th>%s</th>' % col
    html += '</tr></thead><tbody>'
    for element in elements:
        html += '<tr>'
        for col in body:
            html += '<td>%s</td>' % getattr(element, col)
        html += '</tr>'
    html += '</tbody></table>'
    return html

class Table:
    _header = None
    _body = None
    _css_class = None
    _elements = None

    def __init__(self):
        pass

    def thead(self, header):
        self._header = header
        return self

    def tbody(self, body):
        self._body = body
        return self

    def css_class(self, value):
        self._css_class = value
        return self

    def rows(self, elements):
        self._elements = elements
        return self

    def build(self):
        return _html_table(self._header, self._body, self._elements, self._css_class)