import tkinter as tk
from PIL import Image, ImageTk

RADIUS = 20

class window(tk.Frame):
    def __init__(self,root,name):
        global image # we need it because tkinters image handler has some bug in it...
        super().__init__(root)
        self.root = root
        self.name = name
        root.title("Próba GUI")
        img = Image.open('OpenOffice.png')
        image = ImageTk.PhotoImage(img)
        w=img.size[0]
        h=img.size[1]
        root.geometry(f"{w}x{h}")
        root.minsize(width=200, height=200)
        self.isMoving = False
        self.canvas = tk.Canvas(width = 1000, height=550, bg='white')
        self.canvas.pack(expand=tk.YES)
        
        self.canvas.create_image(0,0,image = image, anchor=tk.NW)
        self.circle = self.canvas.create_oval(20,20,60,60,fill="blue")
        #canvas.create_rectangle(0,0,250,170,fill="blue")
        self.my_label = tk.Label(self,text="")#just for testing
        self.my_label.pack()
        
        self.canvas.bind('<B1-Motion>',self.move) #"drag-and-drop" action
        self.canvas.bind('<ButtonRelease-1>',self.release) #when you relase the left mose button
        self.create_rooms()
        self.create_users()
        
        
    def create_rooms(self): #init rooms
        self.rooms = []
        room1 = Room(0,0,250,170)
        room2 = Room(246,15,400,160)
        self.rooms.append(room1)
        self.rooms.append(room2)

    def create_users(self):#init users
        self.you = User(self.name, self.rooms[0]) #The actual user
        self.users=[]
        self.users.append(self.you)

    def move(self,e):
        pos = self.canvas.coords(self.circle)
        if e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3]:
            self.my_label.config(text=f"Coordinates: x: {e.x} y: {e.y}")
            self.canvas.coords(self.circle,e.x-RADIUS,e.y-RADIUS,e.x+RADIUS,e.y+RADIUS)
            self.isMoving = True
    def release(self,e):
        if self.isMoving:
            #print(e)
            for i in self.rooms:
                if e.x>=i.tlx and e.x<=i.brx and e.y>=i.tly and e.y <=i.bry:
                    self.canvas.coords(self.circle,i.center[0]-RADIUS, i.center[1]-RADIUS,i.center[0]+RADIUS, i.center[1]+RADIUS)
                    self.you.move_to(i)
                    self.my_label.config(text=f"{self.you.name} is in room: {self.you.room.id}")
                    break
            self.isMoving = False
class Room():
    id = 0
    def __init__(self,tlx,tly,brx,bry):
        self.tlx=tlx #top left corner
        self.tly=tly
        self.brx=brx
        self.bry=bry
        self.center = ((tlx+brx)/2 , (tly+bry)/2)
        self.id = Room.id
        Room.id += 1
        self.workers = []
    def add_worker(self, worker):
        self.workers.append(worker)
        worker.room=self
    def remove_worker(self,worker):
        self.workers.remove(worker)

class User():
    id = 0
    def __init__(self,name,where):
        self.name = name
        self.room = where
        self.id = User.id
        User.id += 1
        where.add_worker(self)
    def move_to(self,where):
        self.room.remove_worker(self)
        self.room = where
        where.add_worker(self)

class name_input_window(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        root.title("Próba GUI")
        root.geometry("600x400")
        root.minsize(width=200, height=200)
        self.label = tk.Label(root, text="Enter your name: ")
        self.label.pack()
        self.entry = tk.Entry(root)
        self.entry.pack()
        self.button = tk.Button(root, text="OK", command=self.ok)
        self.button.pack()
        self.root.bind('<Return>', self.ok)
    def ok(self,event):
        if len(self.entry.get())>0:
            self.name=self.entry.get()
            self.root.destroy()
        else:
            print("You must write a name in!")

if __name__ == '__main__':
    input_form = tk.Tk() #Starting a form where we ask for the name of the user
    input_window = name_input_window(input_form)
    input_window.pack()
    input_form.mainloop()
    name = input_window.name
    del input_form #We dont need it anymore
    root = tk.Tk() #Starting the main application
    mainWindow = window(root, name)
    mainWindow.pack()
    root.mainloop()