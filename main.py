from typing import List, Union
import discord
import minescript as mc
import asyncio
import json

import pyautogui as ahk

# need to use a config file because env variables dont work with minescript
with open("minecord.json") as cfg_file:
    config = json.load(cfg_file)
    try:
        prefix = config["prefix"]
    except Exception:
        prefix = ";"
    try:
        token = config["token"]
    except Exception:
        mc.echo("couldnt access token in config file")
        exit(-1)
    channel_id = int(config["channel_id"])

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    mc.echo(f"logged in as {bot.user}")


async def process_command(command: List[str], user: str) -> Union[str, None]:
    match command[0][1:]:  # use [1:] to remove the prefix
        case "help":
            return """commands:
    help - list all commands
    move [wasd] [optional seconds<10] - move in a direction for the specified amount of time
    attack [optional seconds<10] - press the left mouse button for the specified amount of time
    use - press the right mouse button
    jump [optional seconds<10] - duh
    look [left,right,up,down] [degrees] - look in the specified direction
    hotbar [1-9] - select the given hotbar slot
    inventory - open or close the inventory (use this to close other guis as well)
    mouse [left,right,up,down] [pixels] - move the mouse (use for guis)
    click [left,right] - send a mouse click (use for guis)"""
        case "move":
            try:
                time = float(command[2])
            except Exception:  # default to 1 second if time not specified
                time = 1
            if time > 10:
                time = 10
            match command[1][0]:
                case "w":
                    mc.player_press_forward(True)
                    await asyncio.sleep(time)
                    mc.player_press_forward(False)
                case "a":
                    mc.player_press_left(True)
                    await asyncio.sleep(time)
                    mc.player_press_left(False)
                case "s":
                    mc.player_press_backward(True)
                    await asyncio.sleep(time)
                    mc.player_press_backward(False)
                case "d":
                    mc.player_press_right(True)
                    await asyncio.sleep(time)
                    mc.player_press_right(False)
                case _:
                    return "invalid usage, 2nd command must be w,a,s,d"
            mc.echo(f"{user} pressed {command[1][0]} for {time} seconds")
        case "attack":
            try:
                time = float(command[1])
            except Exception:
                time = 0.1
            if time > 10:
                time = 10
            mc.player_press_attack(True)
            await asyncio.sleep(time)
            mc.player_press_attack(False)
            mc.echo(f"{user} attacked")
        case "use":
            mc.player_press_use(True)
            mc.player_press_use(False)
            mc.echo(f"{user} used the held item")
        case "jump":
            try:
                time = float(command[1])
            except Exception:
                time = 0.1
            if time > 10:
                time = 10
            mc.player_press_jump(True)
            await asyncio.sleep(time)
            mc.player_press_jump(False)
            mc.echo(f"{user} pressed jump")
        case "look":
            look = mc.player_orientation()
            try:
                magnitude = float(command[2])
            except Exception:
                magnitude = 90
            match command[1]:
                case "left":
                    look[0] -= magnitude
                case "right":
                    look[0] += magnitude
                case "up":
                    look[1] -= magnitude
                case "down":
                    look[1] += magnitude
                case _:
                    return "invalid usage, 2nd command must be left,right,up,down"
            mc.player_set_orientation(*look)
            mc.echo(f"{user} looked {command[1]} {magnitude} degrees")
        case "hotbar":
            try:
                slot = int(command[1]) - 1  # sub 1 because minescript uses 0 indexed
            except Exception:
                return "you must specify a valid slot"
            mc.player_inventory_select_slot(slot)
            mc.echo(f"{user} selected hotbar slot {slot + 1}")
        case "inventory":
            ahk.keyDown("e")
            await asyncio.sleep(0.1)
            ahk.keyUp("e")
            mc.echo(f"{user} toggled inventory")
        case "mouse":
            try:
                magnitude = float(command[2])
            except Exception:
                magnitude = 100
            match command[1]:
                case "left":
                    ahk.moveRel(-magnitude, 0, 0.2)
                case "right":
                    ahk.moveRel(magnitude, 0, 0.2)
                case "up":
                    ahk.moveRel(0, -magnitude, 0.2)
                case "down":
                    ahk.moveRel(0, magnitude, 0.2)
                case _:
                    return "invalid usage, 2nd command must be left,right,up,down"
            mc.echo(f"{user} moved mouse {command[1]} {magnitude}")
        case "click":
            match command[1]:
                case "left":
                    ahk.leftClick()
                case "right":
                    ahk.rightClick()
                case _:
                    return "invalid usage, you must specify a mouse button to click"
            mc.echo(f"{user} pressed {command[1]} click")


@bot.event
async def on_message(message):
    author = message.author
    if author == bot.user:
        return
    if message.channel.id != channel_id:
        return
    text = message.content
    if text[0] == prefix:
        command = text.split(" ")
        result = await process_command(command, author.display_name)
        if result is None:
            return
        else:
            await message.reply(result)
    else:
        return


bot.run(token)
