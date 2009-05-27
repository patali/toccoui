from __future__ import with_statement

# PYMT Plugin integration
IS_PYMT_PLUGIN = True
PLUGIN_TITLE = 'Media Viewer'
PLUGIN_AUTHOR = 'Team'
PLUGIN_ICON = '../mediaviewer/mediaviewer.png'

from pymt import *
from pyglet.media import *
from pymt.ui.widgets.videowidget import *
import random


class Collection(MTWidget):
    def __init__(self, **kwargs):
        super(Collection, self).__init__(**kwargs)
        self.win = kwargs.get('win')
        video = MTVideo(video='../mediaviewer/super-fly.avi',pos=(450,400))
        self.add_widget(video)
        for i in range (5):
            img_src = '../mediaviewer/images/IMG'+str(i)+'.jpg'
            x = int(random.uniform(100, self.win.width-100))
            y = int(random.uniform(100, self.win.height-100))
            rot = random.uniform(0, 360)
            b = MTScatterImage(filename=img_src, pos=(x,y), size=(320,240), rotation=rot)
            self.add_widget(b)

def pymt_plugin_activate(w, ctx):
    ctx.col = Collection(win=w)
    w.add_widget(ctx.col)

def pymt_plugin_deactivate(w, ctx):
    w.remove_widget(ctx.col)


#start the application (inits and shows all windows)
if __name__ == '__main__':
    w = MTWindow(color=(0,0,0,1))
    ctx = MTContext()
    pymt_plugin_activate(w, ctx)
    runTouchApp()
    pymt_plugin_deactivate(w, ctx)      
