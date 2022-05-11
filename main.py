import os

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer

from collections import deque

import database

os.environ['KIVY_VIDEO'] = 'ffpyplayer'


def time_to_ms(time: int) -> (int, int):
    m = str(time // 60).rjust(2, '0')
    s = str(time % 60 + 1).rjust(2, '0')
    return m, s


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

        video_link, time = el['link'].split('#t=')
        start, finish = map(time_to_ms, list(map(int, time.split(','))))

        self.label.text = f"{el['content']}\n\n" \
                          f"Start time: {':'.join(start)}\n" \
                          f"End time: {':'.join(finish)}"
        self.video.source = video_link

    def nothing(self):
        self.label.text = 'NOTHING FOUND'
        self.video.source = ''

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
