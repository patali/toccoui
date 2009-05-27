from __future__ import with_statement


from pymt import *
from pyglet.media import *
from pymt.ui.widgets.videowidget import *
import random

if __name__ == '__main__':
    w = MTWindow()
    kin = MTKinetic()
    video3 = MTVideo(video='super-fly.avi',pos=(450,400))
    kin.add_widget(video3)
    w.add_widget(kin)
    for i in range (5):
        img_src = 'images/IMG'+str(i)+'.jpg'
        x = int(random.uniform(100, w.width-100))
        y = int(random.uniform(100, w.height-100))
        rot = random.uniform(0, 360)
        kin = MTKinetic()
        b = MTScatterImage(filename=img_src, pos=(x,y), size=(320,240), rotation=rot)
        kin.add_widget(b)
        w.add_widget(kin)
        
    exitbut = MTImageButton(filename="exit.png")
    exitbut.x = int(w.width-exitbut.width)
    exitbut.y = int(w.height-exitbut.height)    
    w.add_widget(exitbut)
    @exitbut.event    
    def on_press(touchID, x, y):
        sys.exit()
    runTouchApp()        
