import os

# PYMT Plugin integration
IS_PYMT_PLUGIN = True
PLUGIN_TITLE = 'Video Puzzle'
PLUGIN_AUTHOR = 'Team'
PLUGIN_ICON = os.path.join('..', 'puzzle', 'puzzle.png')


from pymt import *
from pyglet import *
from pyglet.media import *
from pyglet.gl import *
import random


puzzle_register = {}

#A snappable grid layout which produces a container to hold the snappable objects            
class MTSnappableGrid(MTGridLayout):
    def __init__(self, **kwargs):
        super(MTSnappableGrid, self).__init__(**kwargs)
        self.block_size = kwargs.get('block_size')
        self.gridHolders = {}
        for i in range(self.rows*self.cols):
            self.gridHolders[i] = MTRectangularWidget(size=(self.block_size[0],self.block_size[1]),bgcolor=(0.5,0.5,0.5))
            self.add_widget(self.gridHolders[i])    

#A snappable object which snaps into position in the grid            
class MTSnappableWidget(MTWidget):
    def __init__(self, **kwargs):
        super(MTSnappableWidget, self).__init__(**kwargs)       
        self.state = ('normal', None)
        self.grid = kwargs.get('grid')
        global puzzle_register
        
    def on_touch_down(self, touch):
        if self.collide_point(touch.x,touch.y):
            self.bring_to_front()
            self.state = ('dragging', touch.id, touch.x, touch.y)
            return True

    def on_touch_move(self, touch):
        if self.state[0] == 'dragging' and self.state[1] == touch.id:
            self.x, self.y = (self.x + (touch.x - self.state[2]) , self.y + touch.y - self.state[3])
            self.state = ('dragging', touch.id, touch.x, touch.y)
            return True

    def on_touch_up(self, touch):
        if self.state[1] == touch.id:
            self.state = ('normal', None)
            for i in range(self.grid.rows):
                for j in range(self.grid.cols):
                    if(((self.center[0]>=int(self.grid.x+self.width*j)) & \
                    (self.center[0]<=int(self.grid.x+self.width+self.width*j))) &\
                    ((self.center[1]>=int(self.grid.y+self.height*i)) & \
                    (self.center[1]<=int(self.grid.y+self.height+self.height*i)))
                    ):
                        self.center = int(self.grid.x+self.width*j+self.width/2),int(self.grid.y+self.height*i+self.height/2)
                        if self.center == (self.prob_centerX,self.prob_centerY):
                            puzzle_register[self.puzz_id] = 1                          
            self.checkPuzzle_status()                
            return True
            
    def checkPuzzle_status(self):
        zero_count = 0
        for i in range(self.grid.rows*self.grid.cols):
            if puzzle_register[i] == 0 :
                zero_count+=1
        if zero_count>0:
            return
        else:            
            self.parent.player.pause()
            
class PyzzleEngine(MTWidget):
    def __init__(self, **kwargs):
        super(PyzzleEngine, self).__init__(**kwargs)
        global puzzle_register
        self.pieces  = {}
        self.rows = kwargs.get('rows')
        self.cols = kwargs.get('cols')
        self.win = kwargs.get('win')
        self.player = Player()
        self.player.volume = 0.5
        self.source = pyglet.media.load(os.path.join('..', 'puzzle', 'super-fly.avi'))
        self.sourceDuration = self.source.duration
        self.player.queue(self.source)
        self.player.eos_action = 'loop'
        self.width = self.player.get_texture().width
        self.height = self.player.get_texture().height
        self.player.play()
        puzzle_seq = pyglet.image.ImageGrid(self.player.get_texture(),self.rows,self.cols)
        
        self.griddy = MTSnappableGrid(rows=self.rows,cols=self.cols,spacing=0,block_size=(puzzle_seq[0].width,puzzle_seq[1].height))
        self.add_widget(self.griddy)

        self.griddy.pos = (int(self.win.width/2)-300,150)        
        z = 0
        for i in range(self.griddy.rows):
            for j in range(self.griddy.cols):
                self.pieces[z] = PyzzleObject(image=puzzle_seq[z],grid=self.griddy)
                self.pieces[z].prob_centerX = int(self.griddy.x+self.pieces[z].width*j+self.pieces[z].width/2)
                self.pieces[z].prob_centerY = int(self.griddy.y+self.pieces[z].height*i+self.pieces[z].height/2)
                self.pieces[z].puzz_id = z
                self.add_widget(self.pieces[z])
                puzzle_register[z]=0                
                z+=1
                

class PyzzleObject(MTSnappableWidget):
    def __init__(self, **kwargs):
        super(PyzzleObject, self).__init__(**kwargs)
        self.image = kwargs.get('image')
        self.x = int(random.uniform(100, 800))
        self.y = int(random.uniform(100, 600))
        self.width = self.image.width
        self.height = self.image.height
        self.prob_centerX = 0
        self.prob_centerY = 0
        self.puzz_id = 0

    def draw(self):
        glPushMatrix()
        glColor4f(1,1,1,1)
        self.image.blit(self.x,self.y,0)
        glPopMatrix()

def pymt_plugin_activate(w, ctx):
    ctx.pyzzle = PyzzleEngine(rows=3,cols=3,win=w)
    w.add_widget(ctx.pyzzle)


def pymt_plugin_deactivate(w, ctx):
    w.remove_widget(ctx.pyzzle)


if __name__ == '__main__':
    w = MTWindow(color=(0,0,0,1))
    ctx = MTContext()
    pymt_plugin_activate(w, ctx)
    runTouchApp()
    pymt_plugin_deactivate(w, ctx)

 
