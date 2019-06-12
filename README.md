# IRG Lunch Assignment
Code for a website to randomly assign people to host the group lunch, weighted by how often they attend.

A database stores items of type Person, HostAction, and GuestAction. HostActions and GuestActions each have a Person and a date.
The website calculates the Tuesdays in the current or coming month, then randomly assigns a Person to host each Tuesday. The probability 
of a Person being assigned as host increases with the number of times a Person has attended lunch as a guest, and decreases 
(modulo a coefficient) with the number of times a Person has hosted lunch. To prevent one Person from being assigned to host
consecutive lunches, there is a minimum number of days between the last time a Person hosted lunch and when
they can be assigned to host lunch again. To account for visitors, the algorithm assigns as hosts only Persons designated 'active'.

Each lunch instance has its own page, listing the host and any guests. Guests are added on the lunch instance page.
A guest can be any Person. The guest can also add a note relevant to their attendance, ie 'vegetarian'. The lunch instance 
page also allows the host to be reassigned manually.

To prevent unauthorized access, the website requires a login. Anybody with the login can edit HostActions, and add GuestActions,
or Persons.

Future work: the website does not account for holidays.
