import sys
from math import sqrt
from pymt import *
from pyglet.gl import *
from PIL import Image 
from pyglet.image import ImageData 
import ImageEnhance
        
        
class ImageScatter(MTScatterWidget):
    def __init__(self, **kwargs):
        # Preserve this way to do
        # Later, we'll give another possibility, like using a loader...
        kwargs.setdefault('filename', 'photo.jpg')
        if kwargs.get('filename') is None:
            raise Exception('No filename given to MTScatterImage')
        kwargs.setdefault('loader', None)

        super(ImageScatter, self).__init__(**kwargs)
        
        self.pim = Image.open(kwargs.get('filename'))
        #pim = pim.filter(ImageFilter.BLUR)
        self.contrast_enh = ImageEnhance.Contrast(self.pim)
        self.pim = self.contrast_enh.enhance(1.0)
        
        self.bright_enh = ImageEnhance.Brightness(self.pim)
        self.pim = self.bright_enh.enhance(1.0)
        
        self.color_enh = ImageEnhance.Color(self.pim)
        self.pim = self.color_enh.enhance(1.0)
        
        self.bdata = self.pim.tostring() 
        self.img = ImageData(self.pim.size[0], self.pim.size[1], 'RGB', self.bdata, pitch=-self.pim.size[0]*3)         
        self.image  = pyglet.sprite.Sprite(self.img)
        self.width = self.pim.size[0]
        self.height = self.pim.size[1]

    def draw(self):
        with gx_matrix:
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

            
class contrastSlider(MTSlider):
    def __init__(self, **kwargs):
        kwargs.setdefault('min', 0.0)
        kwargs.setdefault('max', 2.0)
        kwargs.setdefault('value', 1.0)
        super(contrastSlider, self).__init__(**kwargs)
        kwargs.setdefault('imageObj', None)
        self.imageObj = kwargs.get('imageObj')
        
    def on_value_change(self,value):
        self.imageObj.changeContrast(value)
        
class brightnessSlider(MTSlider):
    def __init__(self, **kwargs):
        kwargs.setdefault('min', 0.0)
        kwargs.setdefault('max', 2.0)
        kwargs.setdefault('value', 1.0)
        super(brightnessSlider, self).__init__(**kwargs)
        kwargs.setdefault('imageObj', None)
        self.imageObj = kwargs.get('imageObj')
        
    def on_value_change(self,value):
        self.imageObj.changeBrightness(value)
        
class colorizeSlider(MTSlider):
    def __init__(self, **kwargs):
        kwargs.setdefault('min', 0.0)
        kwargs.setdefault('max', 5.0)
        kwargs.setdefault('value', 1.0)
        super(colorizeSlider, self).__init__(**kwargs)
        kwargs.setdefault('imageObj', None)
        self.imageObj = kwargs.get('imageObj')
        
    def on_value_change(self,value):
        self.imageObj.changeColorize(value)
            
if __name__ == '__main__':
    w = MTWindow()
    
    IS = ImageScatter()
    w.add_widget(IS)
    
    cplayout = MTGridLayout(rows=4,cols=2,spacing=5)
    w.add_widget(cplayout)
    
    ctlbl = MTFormLabel(label="Contrast")
    cplayout.add_widget(ctlbl)
    sl = contrastSlider(imageObj=IS,orientation="horizontal")
    cplayout.add_widget(sl)
    
    ctlb2 = MTFormLabel(label="Brightness")
    cplayout.add_widget(ctlb2)
    s2 = brightnessSlider(imageObj=IS,orientation="horizontal")
    cplayout.add_widget(s2)
    
    ctlb3 = MTFormLabel(label="Colorize")
    cplayout.add_widget(ctlb3)
    s3 = colorizeSlider(imageObj=IS,orientation="horizontal")
    cplayout.add_widget(s3)
    
    runTouchApp()            