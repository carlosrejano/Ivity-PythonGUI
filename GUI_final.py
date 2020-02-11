import gi
from UidReader import UidReader
from ReadDataServer import ReadDataServer
import CONSTANTS
import threading

gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, Gdk

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
        self.vloginBox.set_name("vloginBox")
        
        self.loginLabel = Gtk.Label(label="PLEASE, LOGIN WITH YOUR UNIVERSITY CARD")
        self.loginLabel.set_name("loginLabel")
        
        
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
        
        style_provider = Gtk.CssProvider()

        style_provider.load_from_path('./estil/estil.css')

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        self.add(self.hloginBox)
        self.show_all()
        
        self.querysBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.topQuerysBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.querysBox.pack_start(self.topQuerysBox, False, False, 0)
        self.welcomeLabel = Gtk.Label()
        self.welcomeLabel.set_markup("<b>Welcome:</b>")
        self.welcomeLabel.set_line_wrap(True)
        self.nameLabel = Gtk.Label(label="error")
        self.nameLabel.set_name("nameLabel")
        #self.nameLabel.override_color(0, Gdk.RGBA(0.0, 1.0, 0.0, 0.0))
        
        
        self.logoutButton = Gtk.Button(label="Logout")
        self.logoutButton.set_name("logoutButton")
        self.logoutButton.connect("clicked", self.logoutClick)
        self.topQuerysBox.pack_start(self.welcomeLabel, False, False, 4)
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
        self.table = Gtk.Grid()
        self.table.set_column_spacing(100)
        self.table.set_column_homogeneous(False)
        columns = len(data)
        rows = len(data[0])
        
        for i in range(columns):
            for j in range(rows):
                label = Gtk.Label()     
                if(j%2 == 0):
                    label.set_name("fila_parella")
                elif(j%2 != 0):
                    label.set_name("fila_imparella")
                    
                label.set_text(data[i][j])
                self.table.attach(label, i, j, 2, 1)
        
        tablename = self.buffer.get_text().split("?")
        self.table.insert_row(0)
        for k in range(len(CONSTANTS.topRows[tablename[0]])):
            label21=Gtk.Label()
            label21.set_name("primera_fila")
            label21.set_text(CONSTANTS.topRows[tablename[0]][k]);  
            self.table.attach(label21,k,0,2,1)
        return self.table
    
    def changeLabelUsername(self, uid):
        self.uid = uid
        server = ReadDataServer(self.uid)
        self.nameLabel.set_text(server.getName(self.uid))
        #self.nameLabel.override_color(0, Gdk.RGBA(0,0,254,1))
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
        
