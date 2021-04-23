# Hack Kosice Marathon: Augmented Reality Office

## Team

**MechaHU**

### Team members

- Bence Fabó, Budapest University of Technology and Economics
- Mihály Makovsky, Budapest University of Technology and Economics
- Gellért Csapodi, Budapest University of Technology and Economics

## Foreword

We would like to present our **Augmented Reality Office application**.😁 It is important to note that our current version operates with limited functionality yet. 🚧

## Description

  Our project focuses on two important areas of **hybrid office systems**: how to allocate office resources optimally and how to set up hybrid working more efficient. 🏢

  As a result of the **Covid home-office wave**, increasing number of companies are forced to reduce available offices spaces in order to save money, and only a part of the workers are allowed to work physically in the office, while the majority will work remotely. Thus flexible weekly schedules become more and more important to avoid crowding in the reduced office spaces and minimising unused spaces to prevent wasting energy and money. Our machine intelligence 🧠 solution provides an algorithm which **creates a weekly schedule** for optimal allocation of the available office spaces. 📋📋

  Our second goal was to synchronise physical and home office work. The mayor challenge is providing a flexible communication channel between groups in the office and home workers. We solve this problem with an innovative **augmented reality office** application, where all workers can log in the same virtual space that mirrors the real office and show their physical location with an avatar. Full virtual participants can use the same space to join the selected group via placing their similar avatar in a room and **start videochat and share progress immediately** even without having a prescheduled meetings.👻🧑‍💼

  These two ideas, office space allocation and AR-office are put together, so that **companies can schedule their weeks, allocate space, track the progress and current working status of the colleagues, and videochat easily within the same application.** 💻

## Prototype

  During the weekend, all colleagues can register for office space for the next week. They can define the day and time intervall they want to be present in the office, and with how many fellow colleagues they want to work together physically in the office. The office allocation algorithm creates a weekly schedule for the next week from the data of the registrations which prevents and overcrowded rooms and ensures the meeting of people who want to work together. The algorithm creates many random schedule-plans, chooses the best via a predefined fitness function and with fine local search. 

  The program is a **server-client communication based graphical user interface**, which works as an **augmented reality office with real and virtual office rooms**. Loged in physical office users have avatars placed into prescheduled rooms, and home office workers in a virtual rooms. All users location is visible for the others. For example, if a home office user wants to ask a quick question from a fellow colleague, he/she simply has to **grab his avatar and place it into the appropriate room. Then, the program starts a videchat immediately between participants, making communication easy even in hybrid offices.** Also available free rooms are evident at glance of the augmented reality office GUI to start a brand new workgroup.

## Presentation

https://youtu.be/HT5upyGcN8Y

## Challenges and accomplishments

During the project work we had to learn a lot of new concepts and solve a plethera of technical problems, this way we gained precious experience along the way.
- To create the office allocation algorithm, we had to implement artificial intelligence.
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
