
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError('Child classes will override this method to render themselves as HTML.')

    def props_to_html(self):
        html_str = ''
        if self.props is None:
            return ''
        for k, v in self.props.items():
            html_str += f' {k}="{v}"'
        return html_str

    def __repr__(self):
        return f'{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})'

