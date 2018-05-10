#BirdBot created by DeathByAutoscroll with some help from others

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import random
import requests
import os
import uuid
import json

#Opening settings in Config file (include a / at the end of your memedir)
with open("config.json") as cfg:
    config = json.load(cfg)
token = config["token"]
memedirectory = config["memedir"]
bot = commands.Bot(command_prefix = "%")
bot.remove_command('help')

#Sends a message with bot details to console
@bot.event
async def on_ready():
	print ("Connected to discord")
	print ("My name is " + bot.user.name)
	print ("With the ID " + bot.user.id)
	print ("--------------------")

@bot.command(pass_context=True)
async def ping(ctx):
	await bot.say(":ping_pong: **| Pong**")
	print (str(ctx.message.author) + " (" + str(ctx.message.author.id) + ") used the PING command")

#Shows some useful useless info about a player or bot
@bot.command(pass_context=True)
async def facts(ctx, user: discord.Member):
	embed = discord.Embed(title="{}'s info".format(user.name), color=0x7442f4)
	embed.set_thumbnail(url=user.avatar_url)
	embed.add_field(name="Username", value=user.name)
	embed.add_field(name="ID", value=user.id)
	embed.add_field(name="Current Status", value=user.status)
	embed.add_field(name="Highest Role", value=user.top_role)
	embed.add_field(name="Time joined", value=user.joined_at)
	await bot.say(embed=embed)
	print (str(ctx.message.author) + " (" + str(ctx.message.author.id) + ") used the FACTS command")

#Shows some useful useless info about a server
@bot.command(pass_context=True)
async def serverfacts(ctx):
	embed = discord.Embed(title="{}'s info".format(ctx.message.server.name), color=0x7442f4)
	embed.add_field(name="Server Name", value=ctx.message.server)
	embed.add_field(name="Server ID", value=ctx.message.server.id)
	embed.add_field(name="Roles", value=len(ctx.message.server.roles))
	embed.add_field(name="Members", value=len(ctx.message.server.members))
	embed.set_thumbnail(url=ctx.message.server.icon_url)
	await bot.say(embed=embed)
	print (str(ctx.message.author) + " (" + str(ctx.message.author.id) + ") used the SERVERFACTS command")

#Make the bot say anything you want! (Please don't say anything rude)
@bot.command(pass_context=True)
async def say(ctx):
	msg = ctx.message.content.split(" ", 1)
	await bot.delete_message(ctx.message)
	if len(msg) > 1:
		await bot.send_message(ctx.message.channel, msg[1])
		print (str(ctx.message.author) + " (" + str(ctx.message.author.id) + ") used the SAY command")
	else:
		await bot.send_message(ctx.message.channel, '**Command usage:** %say `<message>`"')

#View a bad and maybe outdated meme
@bot.command(pass_context=True)
async def meme(ctx):
	memefile = memedirectory + random.choice(os.listdir(memedirectory)) 
	with open(memefile, "rb") as f:
		await bot.send_file(ctx.message.channel, f)
	print (str(ctx.message.author) + " (" + str(ctx.message.author.id) + ") used the MEME command")

#Displays all commands so you don't have to read though the code like you are now :eyes:
@bot.command(pass_context=True)
async def commands(ctx):
	HelpMsg = discord.Embed(title="List of commands/What they do", color=0x7442f4)
	HelpMsg.add_field(name="Ping", value="Pong")
	HelpMsg.add_field(name="Facts", value="Displays info about a user")
	HelpMsg.add_field(name="Serverfacts", value="Displays info about a server")
	HelpMsg.add_field(name="Say", value="Repeats what you type")
	HelpMsg.add_field(name="Meme", value="Get a really outdated meme")
	HelpMsg.add_field(name="Addmeme", value="Add your own memes")
	HelpMsg.add_field(name="Flip", value="Flips a moon and a shark")
	HelpMsg.add_field(name="Commands", value="Shows this thing again")
	HelpMsg.set_thumbnail(url=ctx.message.author.avatar_url)
	await bot.send_message(ctx.message.author, embed=HelpMsg)
	print (str(ctx.message.author) + " (" + str(ctx.message.author.id) + ") used the COMMANDS command")

#Displays help (still trying to remove the default discord help message)
@bot.command(pass_context=True)
async def help(ctx):
	await bot.send_message(ctx.message.author, "BirdBot was created by DeathByAutoscroll with a fair amount of help from others. \nTo see commands, use %commands!")
	print (str(ctx.message.author) + " (" + str(ctx.message.author.id) + ") used the HELP command")

#Add a meme to the bot's folder! Get those old memes outta here
@bot.command(pass_context=True)
async def addmeme(ctx):
	meme_adding = ctx.message.content.split(" ", 1)
	if len(meme_adding) > 1:
		url = meme_adding[1]
		if url.endswith('.png') or url.endswith('.jpg') or url.endswith('.gif') or url.endswith('.mp4'):
			r = requests.get(url, allow_redirects=True)
			end = url[-4:]
			name = str(uuid.uuid4())
			open(memedirectory + name + end, 'wb').write(r.content)
			await bot.send_message(ctx.message.channel, ":white_check_mark: **| Saved meme as " + str(name) + "!**")
			print (str(ctx.message.author) + " (" + str(ctx.message.author.id) + ") saved " + name + end + " using the ADDMEME command")
		else:
			await bot.send_message(ctx.message.channel, "Sorry, that file format is either invalid or currently not supported! If you'd like it added, please dm @DeathByAutoscroll#7617")
	else:
		await bot.send_message(ctx.message.channel, "Usage: %addmeme <Image URL>")

@bot.command(pass_context=True)
async def flip(ctx):
	await bot.send_message(ctx.message.channel, random.choice([":full_moon_with_face: **| Heads**", ":shark: **| Tails**"]))

bot.run(token)