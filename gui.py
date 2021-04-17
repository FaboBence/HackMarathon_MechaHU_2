import tkinter as tk
from PIL import Image, ImageTk

RADIUS = 20
class Room():
    def __init__(self,tlx,tly,brx,bry):
        self.tlx=tlx #top left corner
        self.tly=tly
        self.brx=brx
        self.bry=bry
        self.center = ((tlx+brx)/2 , (tly+bry)/2)

def move(e):
    global isMoving
    pos = canvas.coords(circle)
    if e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3]:
        my_label.config(text=f"Coordinates: x: {e.x} y: {e.y}")
        canvas.coords(circle,e.x-RADIUS,e.y-RADIUS,e.x+RADIUS,e.y+RADIUS)
        isMoving = True
def release(e):
    global isMoving
    global rooms
    if isMoving:
        #print(e)
        for i in rooms:
            if e.x>=i.tlx and e.x<=i.brx and e.y>=i.tly and e.y <=i.bry:
                canvas.coords(circle,i.center[0]-RADIUS, i.center[1]-RADIUS,i.center[0]+RADIUS, i.center[1]+RADIUS)
        isMoving = False


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Próba GUI")
    root.geometry("1000x600")
    root.minsize(width=200, height=200)
    isMoving = False
    canvas = tk.Canvas(width = 1000, height=550, bg='white')
    canvas.pack(expand=tk.YES)
    img = Image.open('OpenOffice.png')
    image = ImageTk.PhotoImage(img)
    w=img.size[0]
    h=img.size[1]
    canvas.create_image(0,0,image = image, anchor=tk.NW)
    circle = canvas.create_oval(20,20,60,60,fill="blue")
    #canvas.create_rectangle(0,0,250,170,fill="blue")
    my_label = tk.Label(root,text="")
    my_label.pack()
    
    canvas.bind('<B1-Motion>',move)
    canvas.bind('<ButtonRelease-1>',release)
    rooms = []
    room1 = Room(0,0,250,170)
    room2 = Room(246,15,400,160)
    rooms.append(room1)
    rooms.append(room2)
    root.mainloop()