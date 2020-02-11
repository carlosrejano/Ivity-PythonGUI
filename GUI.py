import gi
from UidReader import UidReader
from ReadDataServer import ReadDataServer
import CONSTANTS
import threading
import requests

gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk

class Window(Gtk.Window):
    
    def __init__(self):
        Gtk.Window.__init__(self, title="Atenea")

        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(600,400)
        self.set_border_width(5)
        self.set_resizable(False)
        
        # Iniciar sessio
        
        self.hloginBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.vloginBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.hloginBox.pack_start(self.vloginBox, True, True, 0)
        
        self.loginLabel = Gtk.Label(label="Identificació: ")
        self.vloginBox.pack_start(self.loginLabel, True, False, 0)
        
        self.Reader = UidReader(self.changeLabelUsername)
        thread = threading.Thread(target=self.Reader.readUid)
        thread.deamon = True
        thread.start()
        
        
        """self.clearButton = Gtk.Button(label="Clear")
        #self.clearButton.connect("clicked", self.clearClick)
        self.clearButton.connect("clicked", self.on_button_clicked)
        self.vloginBox.pack_start(self.clearButton, True, False, 0)
        """
        
        self.add(self.hloginBox)
        self.show_all()
        
        self.querysBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.topQuerysBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.querysBox.pack_start(self.topQuerysBox, False, False, 0)
        self.welcomeLabel = Gtk.Label(label="Welcome ")
        self.nameLabel = Gtk.Label(label="error")
        self.logoutButton = Gtk.Button(label="Logout")
        self.logoutButton.connect("clicked", self.logoutClick)
        self.topQuerysBox.pack_start(self.welcomeLabel, False, False, 0)
        self.topQuerysBox.pack_start(self.nameLabel, False, False, 0)
        self.topQuerysBox.pack_end(self.logoutButton, False, False, 0)
        self.queryEntry = Gtk.Entry()
        #self.queryEntry.set_text("Enter your query: ")
        self.buffer = self.queryEntry.get_buffer()
        self.isTable = False
        self.queryEntry.connect("activate", self.getInfoFromServer)
        self.querysBox.pack_start(self.queryEntry, True, False, 0)
        
        
        
        
    def getInfoFromServer(self, widget):
        server = ReadDataServer(self.uid)
        thread = threading.Thread(target=server.sendQuery, args=[widget.get_text(), self.displayTable])
        thread.daemon = True
        thread.start()
    
    def displayTable(self, data):
        if self.isTable:
            self.querysBox.remove(self.table)
        table = self.createTable(data)
        self.remove(self.querysBox)
        self.querysBox.pack_end(table, True, True, 0)
        self.isTable = True
        self.add(self.querysBox)
        self.show_all()
    
    def createTable(self, data):
        #data = [['a','b','c'],['d','e','f'],['g','h','i']]
        self.table = Gtk.Grid()
        self.table.set_column_spacing(100)
        self.table.set_column_homogeneous(False)
        columns = len(data)
        rows = len(data[0])
        for i in range(columns):
            for j in range(rows):
                label = Gtk.Label()
                label.set_text(data[i][j])
                self.table.attach(label,i,j, 5, 1)
        
        return self.table
    
    def changeLabelUsername(self, uid):
        self.uid = uid
        name = requests.get("https://pbe41.000webhostapp.com/index.php/students?student_id="+self.uid).json();
        print(name[0][0]);
        self.nameLabel.set_text(name[0][0])
        self.remove(self.hloginBox)
        self.add(self.querysBox)
        self.show_all()
    
    def logoutClick(self, widget):
        if self.isTable:
            self.querysBox.remove(self.table)
        self.queryEntry.set_text("")
        self.remove(self.querysBox)
        self.add(self.hloginBox)
        thread = threading.Thread(target=self.Reader.readUid)
        thread.deamon = True
        thread.start()
        self.show_all()
        
                
if __name__ == '__main__':
    win = Window()
    win.show_all()
    Gtk.main()    
        
