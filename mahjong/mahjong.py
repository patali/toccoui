from pymt import *
from pyglet import *
from pyglet.media import *
from pyglet.gl import *
import random
import glob

class MTGriddy(MTGridLayout):
    def __init__(self, **kwargs):
        super(MTGriddy, self).__init__(**kwargs)
        self.block_size = kwargs.get('block_size')
        self.gridHolders = {}
        for i in range(self.rows*self.cols):
            self.gridHolders[i] = MTRectangularWidget(size=(self.block_size[0],self.block_size[1]),bgcolor=(0,0,0))
            self.add_widget(self.gridHolders[i]) 


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
        
        self.griddy = MTGriddy(rows=5,cols=int(self.num/5),spacing=5,block_size=(128,128))
        self.add_widget(self.griddy)                   
        self.griddy.pos = (int(w.width/2-self.griddy._get_content_width()/2),int(w.height/2-self.griddy._get_content_height()/2))
        
        k = 0
        for i in range(self.griddy.rows):
            for j in range(self.griddy.cols):
                self.mjobjs[k].do_translation = True
                self.mjobjs[k].init_transform((int(self.griddy.x+20+self.mjobjs[k].width*j),int(self.griddy.y+20+self.mjobjs[k].height*i)), 0, 1.0)
                self.mjobjs[k].do_translation = False
                self.add_widget(self.mjobjs[k])
                k+=1             
                


class MJObject(MTScatterWidget):
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
    mahjong = MJEngine(num=15)
    w.add_widget(mahjong)
    runTouchApp()
 
