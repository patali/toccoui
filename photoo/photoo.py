from pymt import *
from pyglet.gl import *
from PIL import Image 
from pyglet.image import ImageData
import ImageEnhance
import os
import random


# PYMT Plugin integration
IS_PYMT_PLUGIN = True
PLUGIN_TITLE = 'Photoo'
PLUGIN_AUTHOR = 'Team'
PLUGIN_ICON = (os.path.join('..', 'photoo', 'photomanip.png'))


class ImageScatter(MTScatterWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('filename', os.path.join('..', 'photoo', 'photo1.jpg'))
        if kwargs.get('filename') is None:
            raise Exception('No filename given to MTScatterImage')
        kwargs.setdefault('loader', None)

        super(ImageScatter, self).__init__(**kwargs)
        
        self.touch_positions = {}
        
        self.pim = Image.open(kwargs.get('filename'))
        self.contrast_enh = ImageEnhance.Contrast(self.pim)
        self.pim = self.contrast_enh.enhance(1.0)
        
        self.bright_enh = ImageEnhance.Brightness(self.pim)
        self.pim = self.bright_enh.enhance(1.0)
        
        self.color_enh = ImageEnhance.Color(self.pim)
        self.pim = self.color_enh.enhance(1.0)
        
        self.sharp_enh = ImageEnhance.Sharpness(self.pim)
        self.pim = self.sharp_enh.enhance(1.0)
        
        self.bdata = self.pim.tostring() 
        self.img = ImageData(self.pim.size[0], self.pim.size[1], 'RGB', self.bdata, pitch=-self.pim.size[0]*3)         
        self.image  = pyglet.sprite.Sprite(self.img)
        self.width = self.pim.size[0]
        self.height = self.pim.size[1]
        
        
    def on_touch_down(self, touch):
        global workimage
        if self.collide_point(touch.x,touch.y):
            if touch.is_double_tap:
                workimage = self
            super(ImageScatter, self).on_touch_down(touch)
            return True

    def draw(self):
        with gx_matrix:
            glColor4f(1,1,1,1)
            drawRectangle((-6,-6),(self.width+12,self.height+12))
            glScaled(float(self.width)/self.image.width, float(self.height)/self.image.height, 2.0)
            self.image.draw()

            
    def changeContrast(self,value):
        self.pim = self.contrast_enh.enhance(value)
        self.bdata = self.pim.tostring() 
        self.img = ImageData(self.pim.size[0], self.pim.size[1], 'RGB', self.bdata, pitch=-self.pim.size[0]*3)         
        self.image  = pyglet.sprite.Sprite(self.img)
    
    def changeBrightness(self,value):
        self.pim = self.bright_enh.enhance(value)
        self.bdata = self.pim.tostring() 
        self.img = ImageData(self.pim.size[0], self.pim.size[1], 'RGB', self.bdata, pitch=-self.pim.size[0]*3)         
        self.image  = pyglet.sprite.Sprite(self.img)
        
    def changeColorize(self,value):
        self.pim = self.color_enh.enhance(value)
        self.bdata = self.pim.tostring() 
        self.img = ImageData(self.pim.size[0], self.pim.size[1], 'RGB', self.bdata, pitch=-self.pim.size[0]*3)         
        self.image  = pyglet.sprite.Sprite(self.img)
        
    def changeSharpness(self,value):
        self.pim = self.sharp_enh.enhance(value)
        self.bdata = self.pim.tostring() 
        self.img = ImageData(self.pim.size[0], self.pim.size[1], 'RGB', self.bdata, pitch=-self.pim.size[0]*3)         
        self.image  = pyglet.sprite.Sprite(self.img)

workimage = ImageScatter()        
            
class contrastSlider(MTSlider):
    def __init__(self, **kwargs):
        kwargs.setdefault('min', 0.0)
        kwargs.setdefault('max', 5.0)
        kwargs.setdefault('value', 1.0)
        super(contrastSlider, self).__init__(**kwargs)
        kwargs.setdefault('imageObj', None)
        
    def on_value_change(self,value):
        global workimage
        workimage.changeContrast(value)
        
class brightnessSlider(MTSlider):
    def __init__(self, **kwargs):
        kwargs.setdefault('min', 0.0)
        kwargs.setdefault('max', 5.0)
        kwargs.setdefault('value', 1.0)
        super(brightnessSlider, self).__init__(**kwargs)
        kwargs.setdefault('imageObj', None)
        
    def on_value_change(self,value):
        global workimage
        workimage.changeBrightness(value)
        
class colorizeSlider(MTSlider):
    def __init__(self, **kwargs):
        kwargs.setdefault('min', 0.0)
        kwargs.setdefault('max', 5.0)
        kwargs.setdefault('value', 1.0)
        super(colorizeSlider, self).__init__(**kwargs)
        kwargs.setdefault('imageObj', None)
        
    def on_value_change(self,value):
        global workimage
        workimage.changeColorize(value)

class sharpnessSlider(MTSlider):
    def __init__(self, **kwargs):
        kwargs.setdefault('min', 0.0)
        kwargs.setdefault('max', 5.0)
        kwargs.setdefault('value', 1.0)
        super(sharpnessSlider, self).__init__(**kwargs)
        kwargs.setdefault('imageObj', None)
        
    def on_value_change(self,value):
        global workimage
        workimage.changeSharpness(value)



def pymt_plugin_activate(w, ctx):
    # add the images
    global workimage
    for i in range (3):
        img_src = os.path.join('..', 'photoo', 'photo'+str(i+1)+'.jpg')
        x = int(random.uniform(100, w.width-100))
        y = int(random.uniform(100, w.height-100))
        size = random.uniform(0.5, 4.1)*100
        rot = random.uniform(0, 360)
        ctx.image = ImageScatter(filename=img_src, pos=(x,y), size=(size,size), rotation=rot)
        w.add_widget(ctx.image)
    workimage = ctx.image
    

    # setup layout for the filter sliders and labels
    ctx.cplayout = MTGridLayout(rows=4,cols=2,spacing=5)
    
    ctx.ctlbl = MTFormLabel(label="Contrast")
    ctx.cplayout.add_widget(ctx.ctlbl)
    ctx.sl = contrastSlider(orientation="horizontal")
    ctx.cplayout.add_widget(ctx.sl)
    
    ctx.ctlb2 = MTFormLabel(label="Brightness")
    ctx.cplayout.add_widget(ctx.ctlb2)
    ctx.s2 = brightnessSlider(orientation="horizontal")
    ctx.cplayout.add_widget(ctx.s2)
    
    ctx.ctlb3 = MTFormLabel(label="Colorize")
    ctx.cplayout.add_widget(ctx.ctlb3)
    ctx.s3 = colorizeSlider(orientation="horizontal")
    ctx.cplayout.add_widget(ctx.s3)
    
    ctx.ctlb4 = MTFormLabel(label="Sharpness")
    ctx.cplayout.add_widget(ctx.ctlb4)
    ctx.s4 = sharpnessSlider(orientation="horizontal")
    ctx.cplayout.add_widget(ctx.s4)

    # setup filter icon and the menu system
    ctx.filterBut = MTImageButton(filename=(os.path.join('..', 'photoo', 'icons', 'filters.jpg')))
    ctx.filterBut.x,ctx.filterBut.y = int(w.width/2-ctx.filterBut.width/2),0
    w.add_widget(ctx.filterBut)
    
    ctx.menuholder = MTRectangularWidget(bgcolor=(0,0,0))
    ctx.menuholder.width = ctx.cplayout._get_content_width()
    ctx.menuholder.height = ctx.cplayout._get_content_height()
    ctx.menuholder.x=ctx.filterBut.x-int(ctx.menuholder.width/2-ctx.filterBut.width/2)
    ctx.menuholder.y=ctx.filterBut.y+ctx.filterBut.height
    ctx.cplayout.pos = ctx.menuholder.pos
    ctx.menuholder.add_widget(ctx.cplayout)
    
    w.add_widget(ctx.menuholder)
    ctx.menuholder.hide()

    @ctx.filterBut.event    
    def on_press(touch):
        ctx.menuholder.show()
        ctx.menuholder.bring_to_front()
        
    @ctx.filterBut.event    
    def on_release(touch):
        ctx.menuholder.hide()


def pymt_plugin_deactivate(w, ctx):
    w.remove_widget(ctx.image)
    w.remove_widget(ctx.cplayout)
    w.remove_widget(ctx.ctlbl)
    w.remove_widget(ctx.sl)
    w.remove_widget(ctx.ctlb2)
    w.remove_widget(ctx.s2)
    w.remove_widget(ctx.ctlb3)
    w.remove_widget(ctx.s3)
    w.remove_widget(ctx.ctlb4)
    w.remove_widget(ctx.s4)
    w.remove_widget(ctx.filterBut)
    w.remove_widget(ctx.menuholder)
	
if __name__ == '__main__':
    w = MTWindow()
    ctx = MTContext()
    pymt_plugin_activate(w, ctx)
    runTouchApp()
