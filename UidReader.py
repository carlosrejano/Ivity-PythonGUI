import threading
from gi.repository import GLib

class UidReader:
    
    def __init__(self, func):
        self.func = func
        
    def readUid(self):
        #uid = rd.readCard()
        uid = input()
        GLib.idle_add(self.func, uid)
    
