# Family Chores

**Family Chores** is a web-based application made for families and groups (kindergartens, schools, play rooms etc.) providing an easy way to manage daily Chores and School classes.

## Video Demo: <https://www.youtube.com/watch?v=4EJNKQjzsIw>

## Description:

The application was created using Python, JavaScript, SQL3, HTML, CSS, Flask, and Bootstrap 5.
With a focus on the back-end part of the application.
Fully optimized to work on mobile phone browsers.

Run the application using the command **_*python -m flask run*_** in terminal window.

It allows a registered _User_ (parent or teacher) to create a **Group** with a name and password.

**Group** features:

- Chore list that users and members can interact with.
- School timetable for each member.
- Group settings

## Group:

Group is the core of the application, it contains all the information and connects different database tables in to a Python class that has multiple functionalities, and it's very practical to use in code.

**Group** can have:

- 1 Creator (**User** making a group)
- up to 10 Admins (**User** who joins a group)
- up to 30 Members

Number of Admins and Members could be increased.
Group contains all the information about the members, chores, admins. It has its own in table in database. Group is loaded from JSON to a custom Python class.

**Group** has a simple interface consisting of **Chores**, **School** and **Group Panel**.

**User** can be _Creator_ or _Admin_ and in one group at the time.

_Creator_ can remove admins from the group, change the group password, or delete a group.
_Admins_ can only add or remove members from the group, change their own password, or leave the current group.

**Member** is created by a **User** inside a group with a given _name_ and _password_ for a login.

### Homepage

Have three navigational items upon first visit **Member login**, **User login** and **Register**
After the first login, users have two options to **Create** or **Join** a group.

#### Register

Page for registering first-time users. It requires a unique, available _username_ with only alphabetic characters and an _email_ that is not already in use and in valid format. _Password_ is case-sensitive and a minimum of 8 characters long.

#### User login

Login page for registered **User**.

#### Member login

Login page for **Member** using 5-digit _group number_,
_member name_ and _member password_ provided by **User**.

#### Create group

Pop out off-canvas for the **Group** creation. _Group name_ doesn't have to be unique, and the _password_ has to be between 6 and 16 characters long.
Successfully creating a group takes the user to a **Group home** page.

#### Join group

A**User** can join an existing group with a _group number_ and _group password_.

### Group home

After logging in, if a **User** is already part of a group, it takes him to a Group home page.
Group Home has two sections, **Chores **and **School**, that can be accessed by **Users** and **Members**.
The third section is **Group Panel** for **Users**

#### Chores:

The page shows a table with chore information and a list of all members of the group.
Table is created using Jinja.
The table is double-sorted by time posted and time completed.
Navigation item _Create chore_ opens up an off-canvas form requesting Chore Title and Description.

**The user** can create chores for all group members to see and interact with, or delete them.
**Members** can mark chores as complete, which will leave their name and time stamp.

#### School:

The page shows the school timetable on the left for the selected member.
The members page on the right contains a button next to each name; Clicking on it results in showing that member's timetable.
Table body is created using JavaScript.

Navigation item _Update school_ opens up a page for editing timetables.

#### Update school

It consists of a drop-down menu with group members names and input table for each school class for six days of the week.
Table is created using Jinja syntax.
**User** can edit any timetable in the group.
**Member** can only edit its own timetable.

### Group Panel

Page with three sections that can only be accessed by **User**. Add member, Member settings, Settings.

#### Add member

Opens up a pop-up form for adding a new member to a group. It requests _name_ first letter is always capital and _password_ 6 to 12 characters long.

#### Member settings

Member settings open up a list of all current group members with _name_, visible _password_, and a delete button for removing a member.
Table is created in JavaScript.

#### Settings

The Settings page is split into two panels

Admin panel

- **Reset User password** visible to both _Creator_ and \_Admin; this requires the old password and new password to be repeated.

- **Delete account** require a repeated **User** password. If the **User** is the creator of the group, the whole **Group** is deleted as well.

- **Leave Group** visible only to an _Admin_, requires **User** password, and remove **User** from a group.

On the right side, _Group number_ with Show/Hide button

Creator's panel

- **Reset Group password**, require the old group password, and repeat the new password.
- **Delete Group** requires a group number and _Creator's_ password. Deletes everything from all database tables connected to this group (chores, members, group)

Right-side _Admin_ list with all current admins in a group, with a delete button allowing the creator to remove any admin.

## Future updates

With more kids using phones, the idea is to make mobile phone applications with more functionality and features.

- Calendar for adding and tracking events, birthdays etc.
- Mini games
- Cross group
