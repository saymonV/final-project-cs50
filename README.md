# Family Chores

**Family Chores** is a web-based application made for families and groups (kindergarten, schools, play rooms etc.) providing an easy way to manage daily Chores and School classes, giving both adults and kids easy way to keep track of daily errands or school tasks.

## Video Demo:

## Description:

Application was created using Python, Java Script, SQL, HTML, CSS, Flask, Bootstrap 5.
With focus on back-end part of the application.
Fully optimized to work on mobile phone browsers.

It allows registered _User_ (parent or teacher) to create a **Group** with name and password.

**Group** features:

- Chore list users and members can interact with.
- School timetable for each member.
- Group settings

## Group:

Group is core of the application, it contains all the information and connects different database information from multiple tables in to a wholesome Python class that have multiple functionalities and it's very practical to use in code.

**Group** can have:

- 1 Creator (**User** making a group)
- up to 10 Admins (**User** who joins a group)
- up to 30 Members

Number of Admins and Members could be increased.

**Group** has a simple interface consisting of **Chores**, **School** and **Group panel**.
**User** can be only in one group at the time.
**Member** is created by **User** inside a group and given a _name_ and _password_ for login.

_Creator_ can remove admins from the group, change group password or delete a group.
_Admins_ can only add or remove members from the group, change their password or leave group.

### Homepage

Have 3 navigational items upon first visit **Member login**, **User login** and **Register**
After first login, user have two options to **Create** or **Join** a group.

#### Register

Page for registering first time user. It requires a unique available _username_ with alphabet characters only, _email_ that is not already in use and in valid format. _Password_ is case-sensitive and minimum 8 characters long.

#### User login

Login page for registered **User**.

#### Member login

Login page for **Member** using 5-digit _group number_,
_member name_ and _member password_ provided by **User**.

#### Create group

Pop out off canvas for the **Group** creation. _Group name_ doesn't have to be unique and the _password_ has to be between 6 and 16 characters long.
Successfuly creating a group takes user to a **Group home** page.

#### Join group

**User** can join existing group with a _group number_ and _group password_.

### Group home

After login, if a **User** is already part of a group it takes him to a Group home page.
Group home have two sections **Chores**, **School** that can be accessed by **Users** and **Members**.
Third section is **Group Panel** for **Users**

#### Chores:

The page shows a table with chore information and list of all members of the group.
Table is created using Jinja.
Table is double sorted by time posted and time completed.
Navigation item _Create chore_ opens up a offcanvas form requesting Chore Title and Description.

**User** can create chores for all group members to see and interact with or delete them.
**Member** can mark chore complete, which will leave their name and time stamp.

#### School:

Page shows school timetable on the left for selected member.
The members page on the right contains a button next to each name clicking on it results in showing that member's time table.
Table body is created using Java Script.

Navigation item Update schools opens up a page for editing time tables.

#### Update school

Consists of drop down menu with group members names and input table for each school class for six days of the week.
Table is created using Jinja syntax.
**User** can edit any timetable in the group.
**Member** can only edit its own timetable.

### Group Panel

Page with 3 sections that can only be accessed by **User**. Add member, Member settings, Settings.

#### Add member

Opens up a popup form for adding a new member to a group. It requests _name_ first letter is always capital and _password_ 6 to 12 characters long.

#### Member settings

Member settings opens up a list of all current group members with _name_, visible _password_ and delete button for removing a member.
Table is created in Java Script.

#### Settings

Settings page is split in two panels

Admin panel

- **Reset User password** visible to both _Creator_ and _Admin_, requires old password and new password repeated.

- **Delete account** requires repeated **User** password. If **User** is creator of the group whole **Group** is deleted as well.

- **Leave Group** visible only to an _Admin_, requires **User** password and remove **User** from a group.

On the right side _Group number_ with Show/Hide button

Creator's panel

- **Reset Group password** requests old group password and repeatead new password.
- **Delete Group** requests group number and _Creator's_ password. Deletes everything from all database tables connected to this group (chores, members, group)

Right side _Admin_ list with all current admins in a group with a delete button allowing creator to remove any admin.

## Future updates

With more kids using phones, idea is to make mobile phone application with more functionalty and features.

- Calendar for adding and tracking events, birthdays etc.
- Mini games
- Cross group
