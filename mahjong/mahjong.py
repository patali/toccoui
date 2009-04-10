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
            self.mjobjs[z] = MJObject(image=file_list[i])
            z+=1
            self.mjobjs[z] = MJObject(image=file_list[i])
            z+=1            
        random.shuffle(self.mjobjs)
        self.griddy = MTGridLayout(rows=self.num,cols=2,spacing=5)
        self.add_widget(self.griddy)
        
        #self.griddy.pos = (int(w.width/2-self.griddy._get_content_width()/2),int(w.height/2-self.griddy._get_content_height()/2))
        
        for i in range(self.num*2):
            self.griddy.add_widget(self.mjobjs[i])
            
            
class MJObject(MTWidget):
    def __init__(self, **kwargs):
        super(MJObject, self).__init__(**kwargs)
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
    w = MTWindow()
    mahjong = MJEngine(num=4)
    w.add_widget(mahjong)
    runTouchApp()
 
