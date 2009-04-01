from __future__ import with_statement
from pymt import *
import pyglet
from pyglet.gl import *
from pyglet.graphics import draw
from pyglet.text import Label
import math

class IconText(MTWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('size', (200,100))
        super(IconText, self).__init__(**kwargs)
        self.label = "Application 2"
        self.pos = kwargs.get('pos')
        self.opacity = 0
        self.color = (255,255,255,self.opacity)
        
    def draw(self):
        glColor4f(1,0,0,1)
        drawLabel(self.label,self.pos,False,self.color)
        
    def printme(self):
        print self.label

def drawLabel(text, pos=(0,0),center=True,textcolor=(255,255,255,75)):
    _standard_label = Label(text='standard Label', font_size=200,bold=True, color=textcolor)
    _standard_label.anchor_x = 'center'
    _standard_label.anchor_y = 'center'
    _standard_label.x = 0
    _standard_label.y = 0
    _standard_label.text = text
    glPushMatrix()
    glTranslated(pos[0], pos[1], 0.0)
    glScaled(0.3,0.3,1)
    _standard_label.draw()
    glPopMatrix()        

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
        self.label = kwargs.get('label')
        self.iconlabel = IconText(pos=(w.width/2,w.height/2+200))
        w.add_widget(self.iconlabel)    
        self.iconlabel.hide()
    def draw(self):
        self.image.x        = self.x
        self.image.y        = self.y       
        self.size           = (self.image.width, self.image.height)
        #
        with DO(gx_blending, gx_enable(GL_TEXTURE_2D)):
            set_color(1, 1, 1, 1)
            drawCover(self.texture.id, pos=(self.x,self.y + 50), size=(self.image.width,self.image.height))
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
        if (self.parent.parent.to_parent(self.x,self.y)[0] >= (w.width/2-128)) & (self.parent.parent.to_parent(self.x,self.y)[0] <= (w.width/2+128)):
            self.y -= 50
            if self.image.scale < 1.0:
                self.image.scale    = self.image.scale+math.sin(math.pi / 2 * 0.06)
            self.width,self.height  = (self.image.width, self.image.height)
            self.iconlabel.label = self.label
            self.iconlabel.show()
            if self.iconlabel.opacity < 100:
                self.iconlabel.opacity = self.iconlabel.opacity+10
                print self.iconlabel.opacity
        else:
            if self.image.scale > 0.5:
                self.image.scale    = self.image.scale-math.sin(math.pi / 2 * 0.06)
            self.width,self.height  = (self.image.width, self.image.height)
            self.iconlabel.hide()
        self.draw()

def drawCover(texture, pos=(0,0), size=(1.0,1.0)):
    with gx_enable(GL_TEXTURE_2D):
        glBindTexture(GL_TEXTURE_2D,texture)
        pos = ( pos[0],pos[1],   pos[0]+size[0],pos[1],   pos[0]+size[0],pos[1]+size[1],  pos[0],pos[1]+size[1] )
        texcoords = (0.0,0.0, 1.0,0.0, 1.0,1.0, 0.0,1.0)
        draw(4, GL_QUADS, ('v2f', pos), ('t2f', texcoords))
        pos2 = ( pos[0],pos[1]-size[1],   pos[0]+size[0],pos[1]-size[1],   pos[0]+size[0],pos[1]+size[1]-size[1],  pos[0],pos[1]+size[1]-size[1] )
        texcoords2 = (0.0,1.0, 1.0,1.0, 1.0,0.0, 0.0,0.0)
        color2 = (0,0,0,0, 0,0,0,0, 0.4,0.4,0.4,0, 0.4,0.4,0.4,0 )
        draw(4, GL_QUADS, ('v2f', pos2), ('t2f', texcoords2), ('c4f', color2))

if __name__ == '__main__':
    w = MTWindow(bgcolor=(0,0,0,1.0),fullscreen=False)
  
    plane = MTScatterPlane(bgcolor=(1,1,1,1.0),do_rotation=False, do_scale=False, do_translation=['x'], size=(1440,300),pos=(-128,w.height/2-150))
    w.add_widget(plane)

    layme = MTBoxLayout(padding=10, spacing=10, color=(0,0,0,1.0))
    plane.add_widget(layme)
    
    layme.add_widget(MTicon(filename = "browser.png",scale=0.5,label="Browser"))
    layme.add_widget(MTicon(filename = "calculator.png",scale=0.5,label="Calculator"))
    layme.add_widget(MTicon(filename = "chat.png",scale=0.5,label="Chat"))
    layme.add_widget(MTicon(filename = "graph.png",scale=0.5,label="Graph"))
    layme.add_widget(MTicon(filename = "settings.png",scale=0.5,label="Settings"))
    layme.add_widget(MTicon(filename = "ipod.png",scale=0.5,label="Ipod"))
    layme.add_widget(MTicon(filename = "maps.png",scale=0.5,label="Maps"))
    layme.add_widget(MTicon(filename = "notes.png",scale=0.5,label="Notes"))
    layme.add_widget(MTicon(filename = "phone.png",scale=0.5,label="Phone"))
    layme.add_widget(MTicon(filename = "weather.png",scale=0.5,label="Weather"))
    
    runTouchApp()
