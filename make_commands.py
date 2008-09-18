import os
import subprocess
import stat
import time


def main():
    #make_shortcut_to_window(1, 600, 600)
    offsets_x = [1410, 1024, 513, 0]
    offsets_y = [50, 413, 776]

    offsets_x.reverse()

    map = [None,
            'q','w','e','r',
            'a','s','d','f',
            'z','x','c','v',]

    i = 1
    for y in offsets_y:
        for x in offsets_x:
            make_shortcut_to_window(i, map[i], x + 200, y - 10)
            i = i+1

def make_shortcut_to_window(id, key, offset_x, offset_y):
    assert( offset_x + offset_y > 0) #ensure nonzero integers
    base_filename = 'mouse-base.py'
    commands_dir = 'commands/'
    f = open(os.path.abspath(os.path.join(commands_dir, base_filename)), 'r')
    command_text = f.read()
    f.close()

    command_text = command_text % {'offset_x':offset_x, 'offset_y':offset_y}
    command_name = str(id)

    command = os.path.abspath(os.path.join(commands_dir, 
                                           'mouse%s.py' % command_name))
    f = open(command, 'w')
    f.write(command_text)
    f.close()
    os.chmod(command, stat.S_IRWXU)

    set_command = "gconftool-2 --set --type string /apps/metacity/keybinding_commands/command_%s '%s'" % (command_name, command)
    set_shortcut = "gconftool-2 --set --type string /apps/metacity/global_keybindings/run_command_%s '<Alt>%s'" % (command_name, key)

    print subprocess.call(set_command, shell=True)
    print subprocess.call(set_shortcut, shell=True)

def make_start_script(name, offsets_x, offsets_y):
    filename = 'commands/%s.py' % name
    f = open(filename, 'w')
    f.write( '''#!/usr/bin/python
import os
import time
import subprocess
def start_terminal(offset_x, offset_y):
    print subprocess.call("gnome-terminal --geometry=80x24+%s+%s" %% (offset_x,
                                                                     offset_y),
                          shell=True)
for x in %s:
    for y in %s:
        time.sleep(.3)
        start_terminal(x, y)
    ''' % ('%s', '%s', offsets_x, offsets_y))
    f.close()
    os.chmod(filename, stat.S_IRWXU)

def start_terminal(offset_x, offset_y):
    print subprocess.call("gnome-terminal --geometry=80x24+%s+%s" % (offset_x,
                                                                     offset_y),
                          shell=True)

if __name__ == '__main__':
    main()

