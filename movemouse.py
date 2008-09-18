import sys
import Xlib.display
import Xlib.ext.xtest
from Xlib import X

def main():
    xobject = XObject()

    #m = Mouse(xobject)
    #m.move_and_click(30,30)
    #m.move_and_click(300,300)


    '''
    # we tell the X server we want to catch keyPress event
    xobject.root.grab_keyboard(1, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)
    xobject.root.change_attributes(event_mask = X.KeyPressMask)

    keys = range(0,1000)
    for keycode in keys:
        xobject.root.grab_key(keycode, 
                      X.AnyModifier, 
                      1,
                      X.GrabModeAsync, 
                      X.GrabModeAsync)

    while 1:
        event = xobject.root.display.next_event()
        if event.type == X.KeyPress:
            keycode = event.detail
            if keycode == 54:
                sys.exit()
            print keycode
    '''


class XObject(object):
    def __init__(self):
        self.display = Xlib.display.Display()
        self.screen = self.display.screen()
        self.root = self.screen.root

class Mouse(object):
    def __init__(self, xobject):
        self.xobject = xobject

    @property
    def display(self):
        return self.xobject.display

    @property
    def screen(self):
        return self.xobject.screen

    @property
    def root(self):
        return self.xobject.root

    def move(self, x, y):
        self.root.warp_pointer(x, y)
        self.display.sync()
    
    def down(self, button=1):
        Xlib.ext.xtest.fake_input(self.display, Xlib.X.ButtonPress, button)
        self.display.sync()
    
    def up(self, button=1):
        Xlib.ext.xtest.fake_input(self.display, Xlib.X.ButtonRelease, button)
        self.display.sync()

    def move_and_click(self, x, y, button=1):
        #TODO: jperla: maybe should move back?
        self.move(x, y)
        self.down(button)
        self.up(button)


if __name__ == '__main__':
    main()

