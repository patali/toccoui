from __future__ import with_statement
from pymt import *
import pyglet
from pyglet.gl import *
from pyglet.graphics import draw
from pyglet.text import Label
import math
import subprocess, sys

plugins = MTPlugins(plugin_paths=['..'])
plugins.search_plugins()

def action_close_menu(menu, w, args):
    pass
    #menu.parent.remove_widget(menu)
    #del menu    

def action_close_all(menu, w, args):
    sys.exit()
    
def action_launch_plugin(menu, w, args):
    name, plugin = args
    win = MTInnerWindow(size=(640,480), pos=w.pos)
    plugins.activate(plugin, win)
    menu.parent.add_widget(win)
    #win.fullscreen() # This will be fixed in core, and work later on.
    action_close_menu(menu, w, None)

# This is the class definattion for text which appears over the icon
class IconText(MTWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('size', (200,100))
        super(IconText, self).__init__(**kwargs)
        self.label = "Application"
        self.pos = kwargs.get('pos')
        self.opacity = 100
        
    def draw(self):
        glColor4f(1,0,0,1)
        drawLabel(self.label,self.pos,False,(255,255,255,self.opacity))


# This is a function which draws the label using pyglet and opengl
def drawLabel(text, pos=(0,0),center=True,textcolor=(255,255,255,75)):
    _standard_label = Label(text='standard Label', font_size=200, bold=True, color=textcolor)
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


# This is a class defination for the Icon object, the object of these classes maintain
# its own properties like size, sense whether its at the center of the screen, change
# the label's opacity, even detected doubletap events    
class MTicon(MTButton):
    def __init__(self, **kwargs):
        kwargs.setdefault('scale', 1.0)
        kwargs.setdefault('filename', None)
        if kwargs.get('filename') is None:
            raise Exception('No filename given to MTicon')

        super(MTicon, self).__init__(**kwargs)
        self.fname = kwargs.get('filename')
        img = pyglet.image.load(kwargs.get('filename'))
        self.image = pyglet.sprite.Sprite(img)
        self.image.x = self.x
        self.image.y = self.y
        self.scale = kwargs.get('scale')
        self.image.scale = self.scale
        self.width,self.height = (self.image.width, self.image.height)
        self.texture = img.get_texture()
        self.label = kwargs.get('label')
        self.iconlabel = IconText(pos=(w.width/2,w.height/2+200))
        w.add_widget(self.iconlabel)
        self.iconlabel.label = self.label
        self.iconlabel.hide()
        self.action = kwargs.get('action')
        self.args = kwargs.get('args')
                
    def draw(self):
        self.image.x = self.x
        self.image.y = self.y       
        self.size = (self.image.width, self.image.height)
        with DO(gx_blending, gx_enable(GL_TEXTURE_2D)):
            set_color(1, 1, 1, 1)
            drawCover(self.texture.id, pos=(self.x,self.y), size=(self.image.width,self.image.height))
        self.parent.do_layout()

    def on_touch_down(self, touch):        
        if self.collide_point(touch.x, touch.y):
            self.iconlabel.show()
            self.start_animations('fadein')
            if touch.is_double_tap:
                self.iconlabel.hide()
                self.action(self.parent, self, self.args)
            return

    def on_touch_move(self, touch):
        return

    def on_touch_up(self, touch):
        self.iconlabel.hide()
        return        

    def on_draw(self):
        if (self.parent.parent.to_parent(self.x,self.y)[0] >= (w.width/2-128)) & (self.parent.parent.to_parent(self.x,self.y)[0] <= (w.width/2+128)):
            self.y -= 50
            if self.image.scale < 1.0:
                self.image.scale = self.image.scale+math.sin(math.pi / 2 * 0.06)
            self.width,self.height = (self.image.width, self.image.height)
            self.iconlabel.label = self.label
            self.iconlabel.show()
            if self.iconlabel.opacity < 100:
               self.iconlabel.opacity = self.iconlabel.opacity+5
        else:
            if self.image.scale > 0.5:
                self.image.scale = self.image.scale-math.sin(math.pi / 2 * 0.06)
                self.iconlabel.opacity = 0
            self.width,self.height = (self.image.width, self.image.height)
            self.iconlabel.hide()
        self.draw()


    """def on_draw(self):
        if (self.parent.parent.to_parent(self.x,self.y)[0] >= (w.width/2-128)) & (self.parent.parent.to_parent(self.x,self.y)[0] <= (w.width/2+128)):
            self.y -= 50
            if self.image.scale < 1.0:
                self.image.scale    = self.image.scale+math.sin(math.pi / 2 * 0.06)
            self.width,self.height  = (self.image.width, self.image.height)
            #self.iconlabel.label = self.label
            #self.iconlabel.show()
            #if self.iconlabel.opacity < 100:
               #self.iconlabel.opacity = self.iconlabel.opacity+5
        else:
            if self.image.scale > 0.5:
                self.image.scale    = self.image.scale-math.sin(math.pi / 2 * 0.06)
                #self.iconlabel.opacity = 0
            self.width,self.height  = (self.image.width, self.image.height)
            #self.iconlabel.hide()
        self.draw()"""

# This is a function which draws the Icons along with reflections
def drawCover(texture, pos=(0,0), size=(1.0,1.0)):
    with gx_enable(GL_TEXTURE_2D):
        glBindTexture(GL_TEXTURE_2D,texture)
        
        # Draw First Cover
        pos = ( pos[0],pos[1],   pos[0]+size[0],pos[1],   pos[0]+size[0],pos[1]+size[1],  pos[0],pos[1]+size[1] )
        texcoords = (0.0,0.0, 1.0,0.0, 1.0,1.0, 0.0,1.0)
        draw(4, GL_QUADS, ('v2f', pos), ('t2f', texcoords))
        
        # Draw Second Cover
        pos2 = ( pos[0],pos[1]-size[1],   pos[0]+size[0],pos[1]-size[1],   pos[0]+size[0],pos[1]+size[1]-size[1],  pos[0],pos[1]+size[1]-size[1] )
        texcoords2 = (0.0,1.0, 1.0,1.0, 1.0,0.0, 0.0,0.0)
        color2 = (0,0,0,0, 0,0,0,0, 0.4,0.4,0.4,0, 0.4,0.4,0.4,0 )
        draw(4, GL_QUADS, ('v2f', pos2), ('t2f', texcoords2), ('c4f', color2))


if __name__ == '__main__':
    w = MTWindow(style={'bg-color':(0,0,0,1)})
    
    plane = MTScatterPlane(bgcolor=(1,1,1,1.0),do_rotation=False, do_scale=False, do_translation=['x'], size=(1440,300),pos=(-128,w.height/2-150))
    kiney = MTKinetic()
    kiney.add_widget(plane)
    w.add_widget(plane)
    
    layme = MTBoxLayout(padding=10, spacing=10, color=(0,0,0,1.0))
    plane.add_widget(layme)

    plist = plugins.list()
    while len(plist):
        name, plugin = plist.popitem()
        infos = plugins.get_infos(plugin)
        icon = MTicon(filename = infos.get('icon'),scale=0.5,label=infos.get('title'),action=action_launch_plugin, args=[name, plugin])
        layme.add_widget(icon)
    
    runTouchApp()
