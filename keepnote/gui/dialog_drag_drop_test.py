"""

    KeepNote
    Drag Drop Testing Dialog

"""

#
#  KeepNote
#  Copyright (c) 2008-2009 Matt Rasmussen
#  Author: Matt Rasmussen <rasmus@alum.mit.edu>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
#


import os

# pygtk imports
import pygtk
pygtk.require('2.0')
#from gtk import gdk
import gtk.glade


# keepnote imports
import keepnote
from keepnote import get_resource


def parse_utf(text):

    # TODO: lookup the standard way to do this
    
    if text[:2] in ('\xff\xfe', '\xfe\xff') or (
        len(text) > 1 and text[1] == '\x00') or (
        len(text) > 3 and text[3] == '\x00'):
        return text.decode("utf16")
    else:
        return unicode(text, "utf8")



class DragDropTestDialog (object):
    """Drag and drop testing dialog"""
    
    def __init__(self, main_window):
        self.main_window = main_window
    
    def on_drag_and_drop_test(self):
        self.drag_win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.drag_win.connect("delete-event", lambda d,r: self.drag_win.destroy())
        self.drag_win.drag_dest_set(0, [], gtk.gdk.ACTION_DEFAULT)
        
        self.drag_win.set_default_size(400, 400)
        vbox = gtk.VBox(False, 0)
        self.drag_win.add(vbox)
        
        self.drag_win.mime = gtk.TextView()
        vbox.pack_start(self.drag_win.mime, False, True, 0)
        
        self.drag_win.editor = gtk.TextView()
        self.drag_win.editor.connect("drag-motion", self.on_drag_and_drop_test_motion)        
        self.drag_win.editor.connect("drag-data-received", self.on_drag_and_drop_test_data)
        self.drag_win.editor.connect("paste-clipboard", self.on_drag_and_drop_test_paste)
        self.drag_win.editor.set_wrap_mode(gtk.WRAP_WORD)
        
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.set_shadow_type(gtk.SHADOW_IN)
        sw.add(self.drag_win.editor)
        vbox.pack_start(sw)
        
        self.drag_win.show_all()
    
    def on_drag_and_drop_test_motion(self, textview, drag_context, x, y, timestamp):
        buf = self.drag_win.mime.get_buffer()
        target = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
        if target != "":
            textview.drag_dest_set_target_list([(target, 0, 0)])
    
    def on_drag_and_drop_test_data(self, textview, drag_context, x, y,
                                   selection_data, info, eventtime):
        textview.get_buffer().insert_at_cursor("drag_context = " + 
            str(drag_context.targets) + "\n")
        textview.stop_emission("drag-data-received")
        
        buf = textview.get_buffer()
        buf.insert_at_cursor("type(sel.data) = " + 
            str(type(selection_data.data)) + "\n")
        buf.insert_at_cursor("sel.data = " +
            repr(selection_data.data)[:1000] + "\n")
        drag_context.finish(False, False, eventtime)            

        
    
    def on_drag_and_drop_test_paste(self, textview):
        clipboard = self.main_window.get_clipboard(selection="CLIPBOARD")
        targets = clipboard.wait_for_targets()
        textview.get_buffer().insert_at_cursor("clipboard.targets = " + 
            str(targets)+"\n")
        textview.stop_emission('paste-clipboard')
        
        buf = self.drag_win.mime.get_buffer()
        target = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
        if target != "":
            clipboard.request_contents(target, self.on_drag_and_drop_test_contents)
    
    def on_drag_and_drop_test_contents(self, clipboard, selection_data, data):
        buf = self.drag_win.editor.get_buffer()
        data = selection_data.data
        buf.insert_at_cursor("sel.targets = " + repr(selection_data.get_targets()) + "\n")
        buf.insert_at_cursor("type(sel.data) = " + str(type(data))+"\n")        
        print "sel.data = " + repr(data)[:1000]+"\n"
        buf.insert_at_cursor("sel.data = " + repr(data)[:5000]+"\n")
