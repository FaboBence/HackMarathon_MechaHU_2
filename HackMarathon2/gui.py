import tkinter as tk
from PIL import Image, ImageTk
import cv2
RADIUS = 20 #radius of the circles, which represents the users

class window(tk.Frame): #This is the main application
    def __init__(self,root,name):
        global image # we need it because tkinters image handler has some bug in it...
        super().__init__(root)
        self.root = root
        self.name = name
        self.unsaved_movement = False
        root.title("Augmented Reality Office")
        root.state('zoomed')
        self.w=self.root.winfo_screenwidth()
        self.h=self.root.winfo_screenheight()
        root.minsize(width=200, height=200)
        self.isMoving = False
        self.img = Image.open('OpenOffice.png')
        [imageSizeWidth, imageSizeHeight] = self.img.size
        self.ratio = min(self.w/imageSizeWidth,self.h/imageSizeHeight) 
        img = self.img.resize((int(imageSizeWidth*self.ratio), int(imageSizeHeight*self.ratio)), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img)
        self.canvas = tk.Canvas(width = self.w, height=self.h, bg='white')
        self.canvas.pack(expand=tk.YES)
        self.bg_img = self.canvas.create_image(0,0,image = image, anchor=tk.NW)
        self.circle = self.canvas.create_oval(20,20,60,60,fill="blue")

        
        self.canvas.bind('<B1-Motion>',self.move) #"drag-and-drop" action
        self.canvas.bind('<ButtonRelease-1>',self.release) #when you relase the left mose button
        self.create_rooms()
        self.create_users()
        self.other_users = []
        #self.canvas.bind("<Configure>", self.on_resize)
    
    def get_user_by_name(self, name):
        for i in self.users:
            if i.name == name:
                return i
        return None

    def delete_other_users(self):#Removing previous state befor refreshing
        try:
            for i in self.other_users:
                self.canvas.delete(i)
            self.other_users = []
        except:
            print("Cant delete")

    def my_position(self): #asking for the position of the current user, and sendig it to the server
        self.unsaved_movement = False
        return {"Name": self.name, "RoomID": self.you.room.id}
    
    def fix_positions(self): #When two people are in the same room, they're circle shouldn't be on the top of eachother
        tmp_list = [self.canvas.coords(self.circle)[0]]
        for i in self.other_users:
            current_coord = self.canvas.coords(i)[0]
            if current_coord not in tmp_list and current_coord-RADIUS not in tmp_list and current_coord+RADIUS not in tmp_list:
                tmp_list.append(i)
            else:
                try:
                    idx = tmp_list.index(current_coord)
                except:
                    try:
                        idx = tmp_list.index(current_coord-RADIUS)
                    except:
                        idx = tmp_list.index(current_coord+RADIUS)
                
                if idx == 0:
                    oc = self.canvas.coords(self.other_users[idx-1])
                    self.canvas.coords(self.other_users[idx-1],oc[0]-RADIUS,oc[1],oc[2]-RADIUS, oc[3])
                    oc = self.canvas.coords(self.circle)
                    self.canvas.coords(self.circle,oc[0]+RADIUS,oc[1],oc[2]+RADIUS, oc[3])
                else:
                    oc = self.canvas.coords(self.other_users[idx-1])
                    self.canvas.coords(self.other_users[idx-1],oc[0]-RADIUS,oc[1],oc[2]-RADIUS, oc[3])
                    oc = self.canvas.coords(i)
                    self.canvas.coords(i,oc[0]+RADIUS,oc[1],oc[2]+RADIUS, oc[3])

    def update_positions(self,positions=None): #updating positinos based on the data we get from the server.
        if len(positions) >0:
            self.delete_other_users()
            for i in positions:
                if i["Name"] == None:
                    continue
                this_user = self.get_user_by_name(i["Name"])
                if this_user == None: #The user doesnt exists yet
                    new_user = User(i["Name"], self.rooms[i["RoomID"]])
                    tmp_room = self.rooms[i["RoomID"]]
                    user_symbol = self.canvas.create_oval(tmp_room.center[0]-RADIUS, tmp_room.center[1]-RADIUS,tmp_room.center[0]+RADIUS, tmp_room.center[1]+RADIUS, fill="green")
                    self.other_users.append(user_symbol)
                    self.users.append(new_user)
                elif i["RoomID"] == this_user.room.id:
                    if i["Name"] == self.name:
                        pass
                    else:
                        tmp_room = self.rooms[i["RoomID"]]
                        user_symbol = self.canvas.create_oval(tmp_room.center[0]-RADIUS, tmp_room.center[1]-RADIUS,tmp_room.center[0]+RADIUS, tmp_room.center[1]+RADIUS, fill="green")
                        self.other_users.append(user_symbol)
                else:
                    if i["Name"] == self.name:
                        if self.unsaved_movement:
                            continue
                        else:
                            tmp_room = self.rooms[i["RoomID"]]
                            cntr = tmp_room.center
                            self.canvas.coords(self.circle,cntr[0]-RADIUS,cntr[1]-RADIUS,cntr[0]+RADIUS,cntr[1]+RADIUS)
                            this_user.move_to(tmp_room)
                    else:
                        tmp_room = self.rooms[i["RoomID"]]
                        user_symbol = self.canvas.create_oval(tmp_room.center[0]-RADIUS, tmp_room.center[1]-RADIUS,tmp_room.center[0]+RADIUS, tmp_room.center[1]+RADIUS, fill="green")
                        self.other_users.append(user_symbol)
                        this_user.move_to(tmp_room)
            self.fix_positions()
    def create_rooms(self): #init rooms
        self.rooms = []
        room1 = Room(0,0,250,170,self.ratio)
        room2 = Room(250,15,400,160,self.ratio)
        room3 = Room(0,170,250,400,self.ratio)
        room4 = Room(250,170,500,500, self.ratio)
        room5 = Room(500,0,700,170, self.ratio)
        self.rooms.append(room1)
        self.rooms.append(room2)
        self.rooms.append(room3)
        self.rooms.append(room4)
        self.rooms.append(room5)

    def create_users(self):#init users
        self.you = User(self.name, self.rooms[0]) #The actual user
        self.users=[]
        self.users.append(self.you)
    
    def on_resize(self, event):#This function currently out of use, because of the later implemented modifications
        global image
        #img = Image.open('OpenOffice.png')
        pos = self.canvas.coords(self.circle)
        [imageSizeWidth, imageSizeHeight] = self.img.size
        ratio = min(event.width/imageSizeWidth,event.height/imageSizeHeight) 
        self.img = self.img.resize((int(imageSizeWidth*ratio), int(imageSizeHeight*ratio)), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(self.img)
        self.canvas.delete("all")
        self.bg_img = self.canvas.create_image(0,0,image = image, anchor=tk.NW)
        
        #print(ratio)
        #del self.circle
        #self.circle = self.canvas.create_oval(int(pos[0]*self.ratio),int(pos[1]*self.ratio),int(pos[2]*self.ratio),int(pos[3]*self.ratio),fill="blue")
        #self.circle = self.canvas.create_oval(pos[:],fill="blue")
        for i in self.rooms:
            i.refresh_size(ratio)
        center = self.you.room.center
        #self.circle = self.canvas.create_oval(int(pos[0]*self.ratio),int(pos[1]*self.ratio),int(pos[2]*self.ratio),int(pos[3]*self.ratio),fill="blue")
        self.circle = self.canvas.create_oval(20,20,60,60,fill="blue")
        self.canvas.coords(self.circle,center[0]-RADIUS, center[1]-RADIUS,center[0]+RADIUS, center[1]+RADIUS)

        
    def move(self,e):
        pos = self.canvas.coords(self.circle)
        if e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3]:
            self.canvas.coords(self.circle,e.x-RADIUS,e.y-RADIUS,e.x+RADIUS,e.y+RADIUS)
            self.isMoving = True
    def release(self,e):
        start_call = None
        if self.isMoving:
            for i in self.rooms:
                if e.x>=i.tlx and e.x<=i.brx and e.y>=i.tly and e.y <=i.bry:
                    self.canvas.coords(self.circle,i.center[0]-RADIUS, i.center[1]-RADIUS,i.center[0]+RADIUS, i.center[1]+RADIUS)
                    self.you.move_to(i)
                    print(f"{self.you.name} is in room: {self.you.room.id}")
                    if len(self.you.room.workers) >1:
                        if self.you.room.workers[0].id == self.you.id:
                            start_call = self.you.room.workers[1]
                        else:
                            start_call = self.you.room.workers[0]
                    self.fix_positions()
                    break
            self.isMoving = False
            self.unsaved_movement = True
            if start_call is not None:
                start_video(self.root,self,start_call.name)
        #!print(self.my_position())
        #!start_video(self.root,self,"start_call.name")
class Room(): #Class for the rooms
    id = 0
    def __init__(self,tlx,tly,brx,bry,ratio=1):
        self.tlx=tlx*ratio #top left corner
        self.tly=tly*ratio
        self.brx=brx*ratio
        self.bry=bry*ratio
        self.center = ((self.tlx+self.brx)/2 , (self.tly+self.bry)/2)
        self.id = Room.id
        Room.id += 1
        self.workers = []
    def add_worker(self, worker):
        self.workers.append(worker)
        worker.room=self
    def remove_worker(self,worker):
        self.workers.remove(worker)

class User(): #Class of the users
    id = 0
    def __init__(self,name,where):
        self.name = name
        self.room = where
        self.id = User.id
        User.id += 1
        where.add_worker(self)
    def move_to(self,where): #moving the user to the given room 
        self.room.remove_worker(self)
        self.room = where
        where.add_worker(self)

class name_input_window(tk.Frame):#We ask for the name of the user
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        global image
        self.root = root
        self.name=None
        root.minsize(width=200, height=200)
        img = Image.open('Log_in.png')
        w=int(img.size[0]/2)
        h=int(img.size[1]/2)
        img = img.resize((w, h), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img)
        root.geometry(f"{w}x{h}")
        root.title("Login")
        
        self.canvas = tk.Canvas(width = w, height=h, bg='white')
        self.canvas.pack(expand=tk.YES)
        self.bg_img = self.canvas.create_image(0,0,image = image, anchor=tk.NW)
        self.entry = tk.Entry(self.canvas,font = "Helvetica 26",justify="center")
        self.canvas.create_window(364,228, width=320, height=45,window=self.entry)
        self.button = tk.Button(root, text="Enter", command=self.ok)
        self.canvas.create_window(364,280, width=160, height=45,window=self.button)
        self.root.bind('<Return>', self.ok)

    def ok(self,event=None): #Cheking the name, and closing the name input window
        if len(self.entry.get())>0:
            self.name=self.entry.get()
            self.root.destroy()
        else:
            print("You MUST enter a name!")

class video_call(tk.Frame):#The frame for the video call (currently it only reads in two pre-recorded video)
    def __init__(self, root,mainWindow, target):
        super().__init__(root)
        self.target = target
        self.root = root
        self.mainWindow = mainWindow
        self.cap1 = cv2.VideoCapture("Bence_videoChat.avi") #Currently it only reads the given video
        self.cap2 = cv2.VideoCapture("Misi_videoChat.avi")
        ret1, frame1 = self.cap1.read()
        ret2, frame2 = self.cap2.read()
        img1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        img2= cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        if ret1:
            img1 = Image.fromarray(img1)
            img1 = ImageTk.PhotoImage(img1)
        else:
            print("An error occured...")
        if ret2:
            img2 = Image.fromarray(img2)
            img2 = ImageTk.PhotoImage(img2)
        else:
            print("An error occured...")
        self.l1=tk.Label(root, image=img1)
        self.l1.pack(side = tk.LEFT, padx=(75,0))
        self.l2=tk.Label(root, image=img2)
        self.l2.pack(side=tk.RIGHT, padx=(0,75))
        self.button = tk.Button(self, text="Finish call",width=10, bg='red', fg='white', command= lambda: finish_call(self,mainWindow))
        self.button.pack(pady=(700,0))
        self.root.after(1000,self.refresh)

    def refresh(self): #The frames are displayed continously
        ret1, frame1 = self.cap1.read()
        img1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        ret2, frame2 = self.cap2.read()
        img2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        if ret1:
            img1 = Image.fromarray(img1)
            img1 = ImageTk.PhotoImage(img1)
            self.l1.configure(image=img1)
            self.l1.image = img1
        else:
            print("An error occured...")
        if ret2:
            img2 = Image.fromarray(img2)
            img2 = ImageTk.PhotoImage(img2)
            self.l2.configure(image=img2)
            self.l2.image = img2
        else:
            print("An error occured...")
        self.root.after(20,self.refresh)

def start_video(root, mainWindow, target): #starting video call
    frame = mainWindow
    frame.canvas.pack_forget()
    frame.pack_forget()
    video_frame = video_call(root,mainWindow, target)
    video_frame.pack()

def finish_call( v_frame,mainWindow): # for closing video call
    frame = v_frame
    frame.cap1.release()
    frame.cap2.release()
    frame.l1.pack_forget()
    frame.l2.pack_forget()
    frame.pack_forget()
    mainWindow.pack()
    mainWindow.canvas.pack()

if __name__ == '__main__':
    input_form = tk.Tk() #Starting a form where we ask for the name of the user
    input_window = name_input_window(input_form)
    input_window.pack()
    input_form.mainloop()
    name = input_window.name
    del input_form #We dont need it anymore
    if name is not None:
        root = tk.Tk() #Starting the main application
        mainWindow = window(root, name)
        mainWindow.pack()
        root.mainloop()