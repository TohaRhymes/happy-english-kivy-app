from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from collections import deque

import database


class MyLayout(BoxLayout):
    label = ObjectProperty()
    video = ObjectProperty()
    text_input = ObjectProperty()

    def __init__(self, **kwargs):
        self.content = []
        self.content_generator = None
        super().__init__(**kwargs)

    def rotate(self, step=1):
        self.content_generator.rotate(step)
        el = self.content_generator[0]
        self.label.text = el['content']
        self.video.text = '\n\n\n' + el['link']

    def nothing(self):
        self.label.text = 'NOTHING FOUND'
        self.video.text = ''

    def next_text(self):
        if len(self.content) > 0:
            self.rotate(1)

    def prev_text(self):
        if len(self.content) > 0:
            self.rotate(-1)
        else:
            self.nothing()

    def search(self):
        query = self.text_input.text

        self.content = database.search(query, 'database.sqlite')
        if len(self.content) > 0:
            self.content_generator = deque(self.content)
            self.next_text()
        else:
            self.nothing()


class TestApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Label:
        self.layout = MyLayout()
        return self.layout


if __name__ == '__main__':
    TestApp().run()
