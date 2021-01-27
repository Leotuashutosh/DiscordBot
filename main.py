import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()


starter_encouragements = [
  "Ashutosh is Stupid", "The maker of this Bot deserves to Die",
  "Even though I am a robot incapable of human feelings, I would like to say fuck off to my maker","You guys are really big dum-dums!"
]


def getQuote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "\n-"+  json_data[0]['a']
  return quote

def getInsult():
  response = requests.get("https://insult.mattbas.org/api/insult")
  return response.text

def update_encourage(enmsg):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(enmsg)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [enmsg]




@client.event

async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  
  if message.content.startswith('$hello'):
    await message.channel.send('Hello, maggot!')
  
  if message.content.startswith('$inspire'):
    quote = getQuote()
    await message.channel.send('We in the mood for inspiration today? Fine! Dumbass'+"\n\n"+quote)
  
  if msg.startswith("$insult"):
    quote = getInsult()
    await message.channel.send(quote)
  
  
  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options+ db["encouragements"]
  if msg.startswith("$personalinsults"):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    enmsg = msg.split("$new ",1)[1]
    update_encourage(enmsg)
    await message.channel.send("New Insult added")  
  
  
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  
  
  if msg.startswith("$help"):
    quote = "List of commands for this bot. Ples provide feedback for better experience.\n$hello-say hello to the bot.\n$inspire-inspirational quotes.\n$insult-for some good ol fashioned insults.\n$new followed by a space and then a  sentence-to add your own insults.\n$personalinsults- see a random personal insult added by you guys.\n$list- see all your personal insults at once."
    await message.channel.send(quote)
  
  

keep_alive()
client.run(os.getenv('TOKEN'))
