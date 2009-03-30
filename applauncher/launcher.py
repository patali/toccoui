'''
WORK UNDER PROGRESS
Please do not change anything :)

Thank You.
 Sharath Patali

'''

from __future__ import with_statement
from pymt import *
import pyglet
from pyglet.gl import *
from pyglet.graphics import draw
import math

class MTicon(MTButton):
    def __init__(self, **kwargs):
        kwargs.setdefault('scale', 1.0)
        kwargs.setdefault('filename', None)
        if kwargs.get('filename') is None:
            raise Exception('No filename given to MTicon')

        super(MTicon, self).__init__(**kwargs)
        self.fname = kwargs.get('filename')
        img                 = pyglet.image.load(kwargs.get('filename'))
        self.image          = pyglet.sprite.Sprite(img)
        self.image.x        = self.x
        self.image.y        = self.y
        self.scale          = kwargs.get('scale')
        self.image.scale    = self.scale
        self.width,self.height  = (self.image.width, self.image.height)
        self.texture = img.get_texture()

    def draw(self):
        self.image.x        = self.x
        self.image.y        = self.y       
        self.size           = (self.image.width, self.image.height)
        #
        with DO(gx_blending, gx_enable(GL_TEXTURE_2D)):
            set_color(1, 1, 1, 1)
            drawCover(self.texture.id, pos=(self.x,self.y + 50), size=(self.image.width,self.image.height))
        self.parent.do_layout()




        self.parent.do_layout()

    def on_touch_down(self, touches, touchID, x, y):
        if self.collide_point(x,y):
            print "Touched"
            print "file: ",self.fname , self.parent.parent.to_parent(self.x,self.y)[0]
            return

    def on_touch_move(self, touches, touchID, x, y):
        return

    def on_touch_up(self, touches, touchID, x, y):
        if self.collide_point(x,y):
            return

    def on_draw(self):
        if (self.parent.parent.to_parent(self.x,self.y)[0] >= (w.width/2-256)) & (self.parent.parent.to_parent(self.x,self.y)[0] <= (w.width/2)):
            self.y -= 50
            if self.image.scale < 1.0:
                self.image.scale    = self.image.scale+math.sin(math.pi / 2 * 0.06)
            self.width,self.height  = (self.image.width, self.image.height)
        else:
            if self.image.scale > 0.5:
                self.image.scale    = self.image.scale-math.sin(math.pi / 2 * 0.06)
            self.width,self.height  = (self.image.width, self.image.height)
        self.draw()

def drawCover(texture, pos=(0,0), size=(1.0,1.0)):
    with gx_enable(GL_TEXTURE_2D):
        glBindTexture(GL_TEXTURE_2D,texture)
        pos = ( pos[0],pos[1],   pos[0]+size[0],pos[1],   pos[0]+size[0],pos[1]+size[1],  pos[0],pos[1]+size[1] )
        texcoords = (0.0,0.0, 1.0,0.0, 1.0,1.0, 0.0,1.0)
        draw(4, GL_QUADS, ('v2f', pos), ('t2f', texcoords))
        pos2 = ( pos[0],pos[1]-size[1],   pos[0]+size[0],pos[1]-size[1],   pos[0]+size[0],pos[1]+size[1]-size[1],  pos[0],pos[1]+size[1]-size[1] )
        texcoords2 = (0.0,1.0, 1.0,1.0, 1.0,0.0, 0.0,0.0)
        color2 = (0,0,0,0.5, 0,0,0,0.5, 0.5,0.5,0.5,0.5, 0.5,0.5,0.5,0.5 )
        draw(4, GL_QUADS, ('v2f', pos2), ('t2f', texcoords2), ('c4f', color2))
        
       
class slideShow(MTWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('scale', 1.0)
        kwargs.setdefault('filename', None)
        if kwargs.get('filename') is None:
            raise Exception('No filename given to MTicon')

        super(slideShow, self).__init__(**kwargs)
        self.fname = kwargs.get('filename')
        img                 = pyglet.image.load(kwargs.get('filename'))
        self.image          = pyglet.sprite.Sprite(img)
        self.image.x        = self.x
        self.image.y        = self.y
        self.scale          = kwargs.get('scale')
        self.image.scale    = self.scale
        self.width,self.height  = (self.image.width, self.image.height)
        self.texture = img.get_texture()
        self.rotation = 45        

    def draw(self):
        global angle
        self.image.x        = self.x
        self.image.y        = self.y
        self.size           = (self.image.width, self.image.height)
        #
        with DO(gx_enable(GL_BLEND),gx_enable(GL_TEXTURE_2D)):

            glColor4f(1, 1, 1, 1)
            glPushMatrix()
            glTranslatef(self.x,self.y,0)
            glTranslated(self.image.width/2.0,self.image.height/2.0, 0)
            glRotatef(self.rotation, 0.0, 1.0, 0.0)
            glTranslated(-self.image.width/2.0,-self.image.height/2.0, 0)
            drawCover(self.texture.id, pos=(0,0), size=(self.image.width,self.image.height))
             glPopMatrix()
        

    def on_touch_down(self, touches, touchID, x, y):
        if self.collide_point(x,y):
            print "Touched"
            return

    def on_touch_move(self, touches, touchID, x, y):
        return

    def on_touch_up(self, touches, touchID, x, y):
        if self.collide_point(x,y):
            return

    def on_draw(self):
        self.rotation = int((self.rotation+1)%360)
        self.draw()        
       


if __name__ == '__main__':
    w = MTWindow(bgcolor=(0,0,0,1.0))
    sshow = slideShow(filename="slideshow.jpg", pos=(w.width-500,w.height - 600),rotation=45)
    w.add_widget(sshow)    
    plane = MTScatterPlane(bgcolor=(1,1,1,1.0),do_rotation=False, do_scale=False, do_translation=['x'], size=(300,300),pos=(0,10))
    w.add_widget(plane)
    layme = MTBoxLayout(padding=10, spacing=10, color=(0,0,0,1.0))
    plane.add_widget(layme)
    layme.add_widget(MTicon(filename = "browser.png",scale=0.5))
    layme.add_widget(MTicon(filename = "calculator.png",scale=0.5))
    layme.add_widget(MTicon(filename = "chat.png",scale=0.5))
    layme.add_widget(MTicon(filename = "graph.png",scale=0.5))
    layme.add_widget(MTicon(filename = "settings.png",scale=0.5))
    layme.add_widget(MTicon(filename = "ipod.png",scale=0.5))
    layme.add_widget(MTicon(filename = "maps.png",scale=0.5))
    layme.add_widget(MTicon(filename = "notes.png",scale=0.5))
    layme.add_widget(MTicon(filename = "phone.png",scale=0.5))
    layme.add_widget(MTicon(filename = "weather.png",scale=0.5))
    runTouchApp()
