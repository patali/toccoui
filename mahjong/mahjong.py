from pymt import *
from pyglet import *
from pyglet.media import *
from pyglet.gl import *
import random
import glob
            
class MJEngine(MTWidget):
    def __init__(self, **kwargs):
        super(MJEngine, self).__init__(**kwargs)
        self.mjobjs  = {} #list which holds the mahjong objects        
        self.num = kwargs.get('num')
        file_list = glob.glob('icons/*.png')
        random.shuffle(file_list)
        z = 0
        for i in range(self.num):
            self.mjobjs[z] = MJObject(size=(128,128))
            self.mjobjs[z].add_widget(MJImage(image=file_list[i]),side="back")           
            z+=1
            self.mjobjs[z] = MJObject(size=(128,128))
            self.mjobjs[z].add_widget(MJImage(image=file_list[i]),side="back")
            z+=1            
        random.shuffle(self.mjobjs)
        
        self.griddy = MTGridLayout(rows=6,cols=6,spacing=5)
        self.add_widget(self.griddy)                   
                
        k = 0
        for i in range(self.num*2):
            self.griddy.add_widget(self.mjobjs[k])
            k+=1  
        self.griddy.pos = (int(w.width/2-self.griddy._get_content_width()/2),int(w.height/2-self.griddy._get_content_height()/2))
                

class MJObject(MTFlippableWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('do_scale', False)
        kwargs.setdefault('do_rotation', False)
        kwargs.setdefault('do_translation', False)
        super(MJObject, self).__init__(**kwargs)
        
    def on_touch_down(self, touches, touchID, x,y):
        if self.collide_point(x,y):
            self.flip()
            
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
            glTranslatef(self.x, self.y, 0)
            glColor4f(1,1,1,1)
            self.image.draw()

       
if __name__ == '__main__':
    w = MTWindow(bgcolor=(0,0,0,0))
    mahjong = MJEngine(num=18)
    w.add_widget(mahjong)
    runTouchApp()
 
