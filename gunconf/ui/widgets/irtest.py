from pgu.gui import widget
from pgu.gui.const import *
from pygame import *

class IrTest(widget.Widget):
    """A widget that renders as a solid block of color.

    Note the color can be changed by setting the 'value' field, and the
    widget will automatically be repainted, eg:

        c = Color()
        c.value = (255,0,0)
        c.value = (0,255,0)

    """
    irvisible = True

    # The pygame Color instance
    _value = None
    _coords = None
    _newVal = None

    def __init__(self,value=None,**params):
        params.setdefault('focusable',False)
        if value != None:
            params['value']=value
        widget.Widget.__init__(self,**params)


    def paint(self,s):
        needsrepaint = False
        if self._newVal and self._newVal['ir'] != 'notVisible':
            if not self.irvisible:
                needsrepaint = True
            self.ifvisible = True
            s.fill(pygame.Color(0,0,0)) # pointer is visible
            color = None
            if self._newVal['ir'] == 'faint':
               color = Color(255,165,0)
            else:
                color = Color(255,0,0)
            self._drawPointer(s, self._newVal['x'],
                              self._newVal['y'], color)
        if self._newVal and self._newVal['ir'] == 'notVisible':
            if self.irvisible:
                needsrepaint = True
            self.ifvisible = False
            s.fill(pygame.Color(255,0,0))
        print(f"Surface is: {s}")
        if needsrepaint:
            pygame.display.update()


    def _drawPointer(self, s, x, y, color=None):
        """ draw pointer """
        print (f"Pre calculation X {x}, Y {y}")
        x = max(1023 - int((1023-x) * s.get_width() / 1023), 0)
        y = max(727 - int(min(y, 727) * s.get_height() / 727), 0)
#        y = max(733 - int(min(y, 733) * s.get_height() / 733), 0)
#        y = max(1023 - int((1023-y) * s.get_height() / 1023), 0)

        print (f"Surface width is {s.get_width()} and height is {s.get_height()}")

        print (f"(x,y) is ({x},{y})")

        rct = pygame.Rect(max(0, x-10), max(0,y-10), 20, 20)

        print(f"Circle colors {color}, {x}, {y}, 10")

        if color:
            pygame.draw.circle(s, color, (x,y), 10)
        else:
            pygame.draw.rect(s, Color(0,0,0), rct)

        return rct


    def update(self,s):
        old = self._value
        new = self._newVal

        rects = []

        if old and old['ir'] != 'notVisible':
            rct = self._drawPointer(s, old['x'], old['y'])
            rects.append(rct)
        if new and new['ir'] != 'notVisible':
            color = Color(255,165,0) if new['ir']=='faint' else Color(255,0,0)
            rct = self._drawPointer(s, new['x'], new['y'], color)
            rects.append(rct)

        self._value = new

        return rects


    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, dct):
        if not self._value or \
                dct['x'] != self._value['x'] or \
                dct['y'] != self._value['y'] or \
                dct['ir'] != self._value['ir']:
            self._newVal = dct
            print(f"New coordinates and ir value {self._newVal}")
            #self.repaint()
            self.reupdate()
