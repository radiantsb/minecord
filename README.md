# Minecord
## what is it?
a python script that uses the minescript mod to allow people in a discord channel to control the game
##how to use
- install the minescript mod on the minecraft instance you wish to use
- move main.py into minecraft-instance/minescript/
- move minecord.json into minecraft-instance/
- configure token to your discord bots token
- configure channel_id to the id of the channel you want the bot to read commands from
- launch minecraft and run \main.py in chat to start the bot, if successful you should see a message saying "logged in as {bot username}"
##commands
help - list all commands
move [wasd] [optional seconds<10] - move in a direction for the specified amount of time
attack [optional seconds<10] - press the left mouse button for the specified amount of time
use - press the right mouse button
jump - duh
look [left,right,up,down] [degrees] - look in the specified direction
hotbar [1-9] - select the given hotbar slot
inventory - open or close the inventory (use this to close other guis as well)
mouse [left,right,up,down] [pixels] - move the mouse (use for guis)
click [left,right] - send a mouse click (use for guis)
