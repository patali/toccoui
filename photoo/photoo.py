from pymt import *
from pyglet.gl import *
from PIL import Image 
from pyglet.image import ImageData 
import ImageEnhance
        
        
class ImageScatter(MTScatterWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('filename', 'photo.jpg')
        if kwargs.get('filename') is None:
            raise Exception('No filename given to MTScatterImage')
        kwargs.setdefault('loader', None)

        super(ImageScatter, self).__init__(**kwargs)
        
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
        
    def changeSharpness(self,value):
        self.pim = self.sharp_enh.enhance(value)
        self.bdata = self.pim.tostring() 
        self.img = ImageData(self.pim.size[0], self.pim.size[1], 'RGB', self.bdata, pitch=-self.pim.size[0]*3)         
        self.image  = pyglet.sprite.Sprite(self.img)

            
class contrastSlider(MTSlider):
    def __init__(self, **kwargs):
        kwargs.setdefault('min', 0.0)
        kwargs.setdefault('max', 5.0)
        kwargs.setdefault('value', 1.0)
        super(contrastSlider, self).__init__(**kwargs)
        kwargs.setdefault('imageObj', None)
        self.imageObj = kwargs.get('imageObj')
        
    def on_value_change(self,value):
        self.imageObj.changeContrast(value)
        
class brightnessSlider(MTSlider):
    def __init__(self, **kwargs):
        kwargs.setdefault('min', 0.0)
        kwargs.setdefault('max', 5.0)
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

class sharpnessSlider(MTSlider):
    def __init__(self, **kwargs):
        kwargs.setdefault('min', 0.0)
        kwargs.setdefault('max', 5.0)
        kwargs.setdefault('value', 1.0)
        super(sharpnessSlider, self).__init__(**kwargs)
        kwargs.setdefault('imageObj', None)
        self.imageObj = kwargs.get('imageObj')
        
    def on_value_change(self,value):
        self.imageObj.changeSharpness(value)        


 
if __name__ == '__main__':
    w = MTWindow()
    
    IS = ImageScatter()
    w.add_widget(IS)
    
    cplayout = MTGridLayout(rows=4,cols=2,spacing=5)
    

    
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
    
    ctlb4 = MTFormLabel(label="Sharpness")
    cplayout.add_widget(ctlb4)
    s4 = sharpnessSlider(imageObj=IS,orientation="horizontal")
    cplayout.add_widget(s4)
    

    filterBut = MTImageButton(filename="icons/filters.jpg")
    filterBut.x,filterBut.y = int(w.width/2),0
    w.add_widget(filterBut)
    
    menuholder = MTRectangularWidget(bgcolor=(0,0,0))
    menuholder.width = cplayout._get_content_width()
    menuholder.height = cplayout._get_content_height()
    menuholder.x=filterBut.x-int(menuholder.width/2-filterBut.width/2)
    menuholder.y=filterBut.y+filterBut.height
    cplayout.pos = menuholder.pos
    menuholder.add_widget(cplayout)
    
    w.add_widget(menuholder)
    menuholder.hide()
    

    
    @filterBut.event    
    def on_press(touchID, x, y):
        menuholder.show()
        menuholder.bring_to_front()
        
    @filterBut.event    
    def on_release(touchID, x, y):
        menuholder.hide()
    
    

    
    runTouchApp()            