from __future__ import unicode_literals
from urllib.request import urlopen
import os
from PIL import Image
from asciimatics.effects import Print
from asciimatics.renderers import FigletText, ColourImageFile
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Label, TextBox, Button, Text
import rule34

rule34 = rule34.Sync()
CurrentPage = []

effects = []


class Browsing(Frame):

    def __init__(self, screen):
        super(Browsing, self).__init__(screen,
                                       height=screen.height,
                                       width=screen.width // 4,
                                       y=screen.height // 2 - 20, x=0)
        self.palette = {
            'background': (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_GREEN),
            "borders": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_GREEN),
            "title": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_GREEN),
            "label": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_GREEN),
            'edit_text': (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_WHITE),
            'focus_edit_text': (Screen.COLOUR_WHITE, Screen.A_BOLD, 46),
            'focus_button': (Screen.COLOUR_WHITE, Screen.A_BOLD, 46),
            'button': (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_GREEN)
        }
        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Label(height=10, label=str(FigletText('Rule 34', 'smslant', screen.width // 4))))
        search = TextBox(height=1, label='Tags', name='search')
        RunSearch = Text(label='Run search...')
        layout.add_widget(search)

        def GetImages():
            posts = rule34.getImages(search.value[0])
            for post in posts:
                CurrentPage.append(post.file_url)
            return 0

        def UpdateImage():
            if RunSearch.value == '' or CurrentPage == []:
                return 0
            else:
                try:
                    Image.open(urlopen(CurrentPage[int(RunSearch.value)])).save('CurrentImg.png')
                    effects.append(Print(
                        screen,
                        ColourImageFile(screen,
                                        filename=r'sexysex.png' if not os.path.isfile(
                                            'CurrentImg.png') else r'CurrentImg.png',
                                        height=screen.height - 3, uni=True),
                        y=0,
                        x=screen.width // 2
                    ))
                    screen.reset()
                    screen.force_update()
                    print(str(effects))
                except Exception as err:
                    print(err, str(effects))
                    return 0
            return 0

        layout.add_widget(Button(text='Search...', on_click=GetImages))
        RunSearch._on_change = UpdateImage
        layout.add_widget(RunSearch)
        self.fix()


def MainThread(screen):
    effects.append(Browsing(screen))
    screen.play([Scene(effects, 100)])


Screen.wrapper(MainThread)
