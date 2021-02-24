from __future__ import unicode_literals

import multiprocessing as thr
import pathlib
from time import sleep
from urllib.request import urlopen

import rule34
from PIL import Image
from asciimatics.effects import Print
from asciimatics.renderers import FigletText, ColourImageFile
from asciimatics.scene import Scene
from asciimatics.screen import Screen, ManagedScreen
from asciimatics.widgets import Frame, Layout, Label, Button, Text

rule34 = rule34.Sync()
CurrentPage = []
Reload = False


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
        search = Text(label='Tags', name='search')
        RunSearch = Text(label='Run search...')
        layout.add_widget(search)

        def GetImages():
            global Reload
            posts = rule34.getImages(search.value)
            for post in posts:
                CurrentPage.append(post.file_url)
                Reload = True
            return 0

        def UpdateImages():
            global Reload
            if RunSearch.value == '' or CurrentPage == []:
                return 0
            else:
                try:
                    Image.open(urlopen(CurrentPage[int(RunSearch.value)])).save('CurrentImg.png')
                    Reload = True
                except:
                    pass
            return 0

        layout.add_widget(Button(text='Search...', on_click=GetImages))
        layout.add_widget(RunSearch)
        layout.add_widget(Button(text='Run...', on_click=UpdateImages))
        self.fix()


def fetchImage(screen, ex):
    if pathlib.Path(r'CurrentImg.png').exists():
        image = ColourImageFile(screen, r'CurrentImg.png', height=screen.height)
    else:
        image = FigletText(text='NO CURRENT IMAGE')
    eff = [Print(screen, image, y=0)]
    eff.extend(ex)
    screen.play([Scene(eff)])


@ManagedScreen
def MainThread(screen):
    global Reload
    while True:
        fetcher = thr.Process(target=fetchImage, daemon=True, args=(screen, [Browsing(screen)]))
        fetcher.start()

        if Reload:
            sleep(1)
            Reload = False
            fetcher.terminate()
        else:
            sleep(30)
            fetcher.terminate()
        screen.force_update()
        screen.refresh()


MainThread()
