# Hack Kosice Marathon: Your project name

## Team

**MechaHU**

### Team members

- Bence Fabó, Budapest University of Technology and Economics
- Mihály Makovsky, Budapest University of Technology and Economics
- Gellért Csapodi, Budapest University of Technology and Economics

## Description

  Our project focuses on two important areas of **hybrid office systems**: how to allocate office resources and how to make hybrid working more efficient. 🏢

  As a result of the **Covid home-office wave**, more and more companies are likely to decide to reduce available offices spaces in order to save money, and only a part of the workers are going to work in the real offices, the majority will work remotely. Making flexible weekly schedules is going to be more and more improtant, companies'll have to find a way to allocate office spaces to avoid crowding in the reduced offices spaces, but prevent unused office spaces which waste energy and money. Our machine intelliegence 🧠 solution provides an algorithm which **creates a weekly schedule** for the available office spaces. 📋📋

  On the other hand, it's hard to make work efficient when some colleagues are present in the office, while others are at home. What's more, the main drawback of home offices is that you don't see what others are working on and you can't **talk to your colleagues quickly**, without having to organize meetings. We solve both of these problems with an innovative **augmented reality office**, where all workers can log in and show their progress and location. Whether you are at home or in the office, you can place your avatar in a room and update your status. If you want to talk to a colleague, you can take a look at the map of the office to find out where he/she currently is. If they are available, you can simply place your avatar next to him to **start videochat immediately** without having to schedule meetings.👻🧑‍💼

  These two ideas, office allocation and AR-office are put together, so that **companies can schedule their weeks, allocate space, track the progress and current working status of the colleagues, and videochat easily with the same programm, featuring machine intelligence and a comfortable GUI.** 🏢

## Protoype

  During the weekend, all colleagues can register for office space for the next week. They have to type in on which day and in which time intervall they want to be present in the office, and with how many fellow colleagues they want to meet in the office. The office allocation algorithm creates a weekly schedule for the next week from the data of the registrations which prevents overcrowded rooms and ensures the meeting of people who want to work together. The algorithm creates many random schedule-plans, chooses the best of them via a predefined fitness function and with fine local search. It finds the optimal one and transfers the schedule to the program.

  The program is a **server-client communication based graphical user interface**, which works as an **augmented reality office with real and virtual office rooms**. If a colleague logs in, he'/she's avatar is placed into the room in which he should be according to the schedule, or in a virtual room if he/she is working from home. You can see the location of all your logged-in colleagues. For example, if someone working from home wants to ask a quick question from a fellow colleague, he/she simply has to **grab his avatar and place it into the rooms in which the other one is working. Then, the program starts a videchat immediately between the two persons, making communication easy even in hybrid offices.** If you want to check whether there are free rooms available, you can simply take a look at the augmented reality office GUI to find free spaces.

## Presentation

*List any links to your presentation or additional materials that you want to share with the judges.*

## Challenges and accomplishments

During the making of our project we had to learn a lot of new concepts and solve a plethera of technical problems, this way we gained precious experience along the way.
- While creating the office allocation algortihm, we got to know many interesting algortihm-possibilities and modern methods to implement machine intelligence for a certain problem.
- The creation of the application was a real challenge, we had to understand and use:
    -  Python ```sockets``` for the server-client communication
    -  ```Selectors``` to make the sockets non-blocking
    -  Serialization of objects with ```json```
    -  ```Tkinter``` for the _Graphical User Interface_
    -  ```Threading``` to speed up our program
    -  ```OpenCV``` for capturing webcam footage, and displaying it on screen

All in all, **we consider this project as a success**, eventhough we could not implement everything we wanted to. The majority of the above listed python libraries were new to us, and this was the first time we created a functioning server application.

## Next steps
Given the **complexity of our idea** there are lot's of further features which are waiting to be implemented:
- Transfering the camera footage with audio over the server is still not implemented because we ran into too many problems.
- We would like to make office space registraion easier via an online questionaire (currently, you have to type your request into a .csv file)
- We would like to further develop the office space allocation algorithm to make it find the optimal schedule quickly, even for bigger, more comlicated office systems. 
- The **augmented reality office** has many more development-possibilities: **working status, file sharing, advanced avatars holding more information, rooms with different roles, etc.**
- The **graphics** could be improved by a large margin, and the above listed functionalities could be implemented.
- For real life applications the server communication must be improved to make it more stable and secure.

## Structure of our project
Currently our program can only be run from a computer with `Python 3.7` downloaded.
- `Main_Client.py` is the Main file, which runs the GUI (`gui.py`), and handles communication with the Server.
- `Main_Server.py` handles the office space allocation algorithm (`Office_allocation.py`), and sets up a Server to which the Clients can connect.
- Inside `Message_Client.py` is the Client 'Message' class which contains all necessary functions.
- Inside `Message_Server.py` is the Server 'Message' class which contains all necessary functions.
- We have experimented with capturing, storing and playing back webcam footage in `recording.py`.
