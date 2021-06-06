import discord
from discord.ext import tasks
from discord.ext import commands
import json
import time


async def start_pings():
    # set variable so it wont get started again
    client.pinging = True
    server = client.get_guild(client.server)
    # if the channel in the db.json is null
    if client.channel is None:
        channel = await server.create_text_channel(str(client.total_channels))
        client.channel = channel.id
    # if there is a valid channel in the db.json
    else:
        channel = client.get_channel(client.channel)

    while True:
        # check if the bot has already sent 10000 pings (i added 50 as a buffer)
        if client.count < 10050:
            await channel.send("@everyone")
            client.count += 1
        else:  # reset the channel
            client.count = 0
            client.total_channels += 1
            channel = await server.create_text_channel(str(client.total_channels))
            client.channel = channel.id


client = commands.Bot(command_prefix='ping', case_insensitive=True)
# initialize the database variables
try:
    with open('db.json') as meow:
        db = json.load(meow)
except FileNotFoundError:  # create the db.json if it doesnt exist already
    db = {
        "count": 0,
        "channel": None,
        "total_channels": 0
    }
    with open('db.json', 'w+') as meow:
        json.dump(db, meow)
        meow.close()
client.count = db["count"]
client.channel = db["channel"]
client.total_channels = db["total_channels"]
client.pinging = False


@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')
    time.sleep(2)
    # make sure they dont get started twice
    if not client.pinging:
        update_json.start()
        await start_pings()


@client.listen('on_message')
async def on_message(message):
    # placeholder in case i wanna do stuff with this
    pass


@client.command()
async def test():
    # also placeholder
    pass


@tasks.loop(minutes=5)
async def update_json():
    # update the db.json every 5 minutes
    # create a dictionary to put inside the db.json
    print('updating db.json...')
    db = {
        "count": client.count,
        "channel": client.channel,
        "total_channels": client.total_channels
    }
    # dump the dictionary into the json file
    with open('db.json', 'w+') as meow:
        json.dump(db, meow)
        meow.close()
    print(f'count: {client.count}\nchannel: {client.channel}\ntotal channels: {client.total_channels}')
    print('successfully updated the database')


with open('config.json') as meow:
    # start the bot
    config = json.load(meow)
    client.server = config["server"]
    client.run(config["token"])
