import tkinter as tk
from PIL import Image, ImageTk

RADIUS = 20

class window(tk.Tk):
    def __init__(self):
        global image # we need it because tkinters image handler has some bug in it...
        super().__init__()
        self.title("Próba GUI")
        img = Image.open('OpenOffice.png')
        image = ImageTk.PhotoImage(img)
        w=img.size[0]
        h=img.size[1]
        self.geometry(f"{w}x{h}")
        self.minsize(width=200, height=200)
        self.isMoving = False
        self.canvas = tk.Canvas(width = 1000, height=550, bg='white')
        self.canvas.pack(expand=tk.YES)
        
        self.canvas.create_image(0,0,image = image, anchor=tk.NW)
        self.circle = self.canvas.create_oval(20,20,60,60,fill="blue")
        #canvas.create_rectangle(0,0,250,170,fill="blue")
        self.my_label = tk.Label(self,text="")
        self.my_label.pack()
        
        self.canvas.bind('<B1-Motion>',self.move)
        self.canvas.bind('<ButtonRelease-1>',self.release)
        self.rooms = []
        room1 = Room(0,0,250,170)
        worker1 = User('Gege', room1)
        print(worker1.room.id)
        print(room1.workers[0].name)
        room2 = Room(246,15,400,160)
        worker1.move_to(room2)
        print(room1.workers)
        print(room2.workers)
        print(worker1.room.id)
        #print(room2.id)
        self.rooms.append(room1)
        self.rooms.append(room2)
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


if __name__ == '__main__':
    root = window()
    root.mainloop()
