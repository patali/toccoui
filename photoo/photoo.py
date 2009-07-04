from pymt import *
from pyglet.gl import *
from PIL import Image 
from pyglet.image import ImageData
import ImageEnhance


# PYMT Plugin integration
IS_PYMT_PLUGIN = True
PLUGIN_TITLE = 'Photoo'
PLUGIN_AUTHOR = 'Team'
PLUGIN_ICON = '../photoo/photoo.png'
       
        
class ImageScatter(MTScatterWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('filename', '../photoo/photo.jpg')
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
        
        
        """self.fbo = Fbo(size=(self.width, self.height), with_depthbuffer=False)
        self.color = (0,1,0,1.0)
        set_brush('brushes/brush_particle.png')
        self.clears()        
        
    def clears(self):
        self.fbo.bind()
        glClearColor(0.75,0.2,0,1)
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(1,1,1,1)
        #self.img.blit(0,0)
        self.fbo.release()"""

        
    def on_touch_down(self, touches, touchID, x, y):
        global workimage
        if self.collide_point(x,y):
            if touches[touchID].is_double_tap:
                workimage = self
            #self.touch_positions[touchID] = (x,y)
            #self.fbo.bind()
            #glColor4f(0,1,0,1)
            #paintLine((x,y,x,y))
            #glColor4f(1,1,1,1)
            #self.fbo.release()
            super(ImageScatter, self).on_touch_down(touches, touchID, x, y)
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
    #add the images
    global workimage
    ctx.image = ImageScatter()
    w.add_widget(ctx.image)
    ctx.image = ImageScatter(filename="../photoo/photo2.jpg")
    w.add_widget( ctx.image)
    ctx.image = ImageScatter(filename="../photoo/photo3.jpg")
    w.add_widget(ctx.image)
    workimage =  ctx.image

    #setup layoyut for the filter sliders and labels
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

    #setup filter icon and the menu system
    ctx.filterBut = MTImageButton(filename="../photoo/icons/filters.jpg")
    ctx.filterBut.x,ctx.filterBut.y = int(w.width/2-ctx.filterBut.width/2),0
    #w.add_widget(ctx.filterBut)
    
    ctx.menuholder = MTRectangularWidget(bgcolor=(0,0,0))
    ctx.menuholder.width = ctx.cplayout._get_content_width()
    ctx.menuholder.height = ctx.cplayout._get_content_height()
    ctx.menuholder.x=ctx.filterBut.x-int(ctx.menuholder.width/2-ctx.filterBut.width/2)
    ctx.menuholder.y=ctx.filterBut.y+ctx.filterBut.height
    ctx.cplayout.pos = ctx.menuholder.pos
    ctx.menuholder.add_widget(ctx.cplayout)
    
    w.add_widget(ctx.menuholder)
    #ctx.menuholder.hide()

    @ctx.filterBut.event    
    def on_press(touchID, x, y):
        ctx.menuholder.show()
        ctx.menuholder.bring_to_front()
        
    @ctx.filterBut.event    
    def on_release(touchID, x, y):
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
    pymt_plugin_deactivate(w, ctx)


"""if __name__ == '__main__':
    w = MTWindow()
    
    #add the images
    image = ImageScatter()
    w.add_widget(image)
    image = ImageScatter(filename="photo2.jpg")
    w.add_widget(image)
    image = ImageScatter(filename="photo3.jpg")
    w.add_widget(image)
    workimage = image
    
    #setup layoyut for the filter sliders and labels
    cplayout = MTGridLayout(rows=4,cols=2,spacing=5)
    
    ctlbl = MTFormLabel(label="Contrast")
    cplayout.add_widget(ctlbl)
    sl = contrastSlider(orientation="horizontal")
    cplayout.add_widget(sl)
    
    ctlb2 = MTFormLabel(label="Brightness")
    cplayout.add_widget(ctlb2)
    s2 = brightnessSlider(orientation="horizontal")
    cplayout.add_widget(s2)
    
    ctlb3 = MTFormLabel(label="Colorize")
    cplayout.add_widget(ctlb3)
    s3 = colorizeSlider(orientation="horizontal")
    cplayout.add_widget(s3)
    
    ctlb4 = MTFormLabel(label="Sharpness")
    cplayout.add_widget(ctlb4)
    s4 = sharpnessSlider(orientation="horizontal")
    cplayout.add_widget(s4)
    
    #setup filter icon and the menu system
    filterBut = MTImageButton(filename="icons/filters.jpg")
    filterBut.x,filterBut.y = int(w.width/2-filterBut.width/2),0
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
        
    exitbut = MTImageButton(filename="exit.png")
    exitbut.x = int(w.width-exitbut.width)
    exitbut.y = int(w.height-exitbut.height)    
    w.add_widget(exitbut)
    @exitbut.event    
    def on_press(touchID, x, y):
        sys.exit()    
    
    

    
    runTouchApp()            
"""
