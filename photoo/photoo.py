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
        self.pim = self.contrast_enh.enhance(1.1)
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
            
class splSlider(MTSlider):
    def __init__(self, **kwargs):
        kwargs.setdefault('min', 0.0)
        kwargs.setdefault('max', 2.0)
        kwargs.setdefault('value', 1.0)
        super(splSlider, self).__init__(**kwargs)
        kwargs.setdefault('imageObj', None)
        self.imageObj = kwargs.get('imageObj')
        
    def on_value_change(self,value):
        self.imageObj.changeContrast(value)
            
if __name__ == '__main__':
    w = MTWindow()
    IS = ImageScatter()
    w.add_widget(IS)
    sl = splSlider(imageObj=IS)
    w.add_widget(sl)
    runTouchApp()            