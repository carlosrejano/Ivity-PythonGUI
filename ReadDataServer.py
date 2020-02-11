from gi.repository import GLib
import requests
import threading

class ReadDataServer:
    def __init__(self, uid):
        self.url = "https://pbe41.000webhostapp.com/index.php/"
        self.uid = uid
    
    def sendQuery(self, query, func):
        txt=query.split("?");
        url = self.url + txt[0]+"?owner_id="+self.uid;
        if len(txt[1])>0:
            url=url+"&"+txt[1];
        data = requests.get(url).json()
        GLib.idle_add(func, data)
    
    def getName(self, uid):
        self.uid = uid
        url = self.url + "students?student_id="+self.uid
        name = requests.get(url).json()
        return name[0][0]

    
