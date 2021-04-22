# Hack Kosice Marathon: Your project name

## Team

**MechaHU**

### Team members

- Bence Fabó, Budapest University of Technology and Economics
- Mihály Makovsky, Budapest University of Technology and Economics
- Gellért Csapodi, Budapest University of Technology and Economics

## Description

Our project focuses on two important areas of hybrid office systems: how to allocate office resources and how to make hybrid working more efficient. 
As a result of the Covid home-office wave, more and more companies are likely to decide to reduce available offices spaces in order to save money, and only a part of the workers are going to work in the real offices, others are going to work from home. Making flexible weekly schedules is going to be more and more improtant, companies'll have to find a way to allocate office spaces to avoid crowding in the reduced offices spaces, but prevent unused office spaces which waste energy and money. Our machine intelliegence solution provides an algorithm which creates a weekly schedules for the available office spaces. 
On the other hand, it's hard to make work efficient when some colleagues are present in the office, while others are at home. What's more, the main drawback of home offices is that you don't see what others are working on and you can't talk to your colleagues quickly, without having to organize meetings. We solve both of these problems with an innovative augmented reality office, where all workers can log in and show their progress and location. Whether you are at home or in the office, you can place your avatar in a room and update your status. If you want to talk to a colleague, you can check on the GUI where he/she currently is, an if he's/she's at home, you can simply place your avatar next to him to start videochat immediately, without having to schedule meetings.
These two ideas, office allocation and AR-office are put together, so that companies can schedule their weeks, allocate space, track colleagues locations and current working status and videochat easily with the same programm, featuring machine intelligence and a comfortable GUI.

## Protoype

During the weekend, all colleagues can register for office space for the next week. They have to type in on which day and in which time intervall they want to be present in the office, and with how many fellow colleagues they want to meet in the office. The office allocation algorithm creates a weekly schedule for the next week from the data of the registrations which prevents overcrowded rooms and ensures the meeting of people how want to work together. The algorithm creates many random schedule-plans, chooses the best of them via a predefined fitness function, and with fine local search, it finds the optimal one and transfers the schedule to the program.
The program is a server-client communication based graphical user interface, which works as an augmneted reality office with online and real office rooms. If a colleague logs in, he'/she's avatar is placed into the room in which he should be according to the schedule, or he/she is put into the online spaces if he/she is working from home. You can see all your logged-in colleagues locations. For example, if someone working from home wants to ask a quick question from a fellow colleague, he/she simply has to grab his avatar and place it into the rooms in which the other one is working. Then, the program starts a videchat immediately between the two person, making communication easy even in hybrid offices. Or, if you want to check whether there are free rooms available, you can simply have a look at the augmented reality ofiice GUI to fnd free spaces.

## How to try

*List any URLs relevant to demonstrating your prototype, e.g. a live url where judges can preview your app. Note that judges won't be able to setup anything in their computers.*

## Presentation

*List any links to your presentation or additional materials that you want to share with the judges.*

## Challenges and accomplishments

*Is there anything unexpected that you learned over the course of this project?*

*Is there something your team is particularly proud of, related to this project?*

## Next steps

*What do you need to do next to turn this prototype into a working solution?*
