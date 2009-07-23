from __future__ import with_statement

# PYMT Plugin integration
IS_PYMT_PLUGIN = True
PLUGIN_TITLE = 'Mahjong Game'
PLUGIN_AUTHOR = 'Team'
PLUGIN_ICON = '../mahjong/mahjong.png'


from pymt import *
from pyglet import *
from pyglet.media import *
from pyglet.gl import *
import random
import glob

tile1 = -1
tile2 = -1
tile_open_count = 0

def check(dt):
        global tile_open_count, tile1, tile2
        if tile1.id == tile2.id:
            tile1.hide()
            tile2.hide()
        else:
            tile1.flip()
            tile2.flip()
        tile_open_count=0
        tile1 = -1
        tile2 = -1
        

class MTPlaceholder(MTRectangularWidget):
    def __init__(self, **kwargs):
        super(MTPlaceholder, self).__init__(**kwargs)
        self.color = kwargs.get('color')
    
    def draw(self):
        set_color(*self.color)
        drawRectangle(pos=self.pos, size=self.size)
        
class MJEngine(MTWidget):
    def __init__(self, **kwargs):
        super(MJEngine, self).__init__(**kwargs)
        self.mjobjs  = {} #list which holds the mahjong objects        
        self.num = kwargs.get('num')
        file_list = glob.glob('../mahjong/icons/*.png')
        random.shuffle(file_list)
        z = 0
        self.win = kwargs.get('win')
        self.placeholder = MTPlaceholder(size=(128,128),color=(1,1,1,1))
        for i in range(self.num):
            self.mjobjs[z] = MJObject(size=(128,128))
            self.mjobjs[z].id = i
            self.mjobjs[z].add_widget(MJImage(image=file_list[i]),side="back")           
            self.mjobjs[z].add_widget(self.placeholder,side="front")
            z+=1
            self.mjobjs[z] = MJObject(size=(128,128))
            self.mjobjs[z].id = i
            self.mjobjs[z].add_widget(MJImage(image=file_list[i]),side="back")
            self.mjobjs[z].add_widget(self.placeholder,side="front")
            z+=1            
        random.shuffle(self.mjobjs)
        
        self.griddy = MTGridLayout(rows=4,cols=5,spacing=5)
        self.add_widget(self.griddy)                   
                
        k = 0
        for i in range(self.num*2):
            self.griddy.add_widget(self.mjobjs[k])
            k+=1  
        self.griddy.pos = (int(self.win.width/2-350),int(100))
        #self.griddy.pos = (int(self.win.width/2-self.griddy._get_content_width()/2),int(self.win.height/2-self.griddy._get_content_height()/2))
                

class MJObject(MTFlippableWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('do_scale', False)
        kwargs.setdefault('do_rotation', False)
        kwargs.setdefault('do_translation', False)
        super(MJObject, self).__init__(**kwargs)
        self.id = 0
        self.flipped = False
        
    def on_touch_down(self, touch):
        global tile_open_count, tile1, tile2,check
        if self.collide_point(touch.x, touch.y):
            if tile_open_count == 0:
                self.flip()
                self.flipped = True
                tile_open_count+=1
                tile1 = self                
            elif tile_open_count == 1:
                if tile1 == self:
                    self.flip()
                    self.flipped = False
                    tile1 = -1
                    tile_open_count = 0
                else:
                    self.flip()
                    self.flipped = True
                    tile_open_count+=1
                    tile2 = self
                    pyglet.clock.schedule_once(check, 0.5)


                
class MJImage(MTWidget):
    def __init__(self, **kwargs):
        super(MJImage, self).__init__(**kwargs)
        self.img_src = kwargs.get('image')
        self.img                 = pyglet.image.load(self.img_src)
        self.image          = pyglet.sprite.Sprite(self.img)        
        self.image.x        = self.x
        self.image.y        = self.y
        self.size           = (self.image.width, self.image.height)

    def draw(self):
        with gx_matrix:
            glColor4f(1,1,1,1)
            glTranslatef(self.x, self.y, 0)            
            self.image.draw()

def pymt_plugin_activate(root, ctx):
    ctx.mahjong = MJEngine(num=10,win = root)
    root.add_widget(ctx.mahjong)

def pymt_plugin_deactivate(root, ctx):
    root.remove_widget(ctx.mahjong)		

if __name__ == '__main__':
    w = MTWindow()
    ctx = MTContext()
    pymt_plugin_activate(w, ctx)
    runTouchApp()
    pymt_plugin_deactivate(w, ctx)	
