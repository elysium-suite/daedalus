from discord.ext import commands
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import discord
import ssl
import os


#       .o8                            .o8            oooo                       
#      "888                           "888            `888                       
#  .oooo888   .oooo.    .ooooo.   .oooo888   .oooo.    888  oooo  oooo   .oooo.o 
# d88' `888  `P  )88b  d88' `88b d88' `888  `P  )88b   888  `888  `888  d88(  "8 
# 888   888   .oP"888  888ooo888 888   888   .oP"888   888   888   888  `"Y88b.  
# 888   888  d8(  888  888    .o 888   888  d8(  888   888   888   888  o.  )88b 
# `Y8bod88P" `Y888""8o `Y8bod8P' `Y8bod88P" `Y888""8o o888o  `V88V"V8P' 8""888P' 


# SPECIFY REMOTE HERE AND YOUR BOT Token HERE
remote = ''
bot_id = ''
# COMMAND PREFIX
client = commands.Bot(command_prefix = 'd ')

def get_time():
	time = 'Score Reported at: {}'.format(datetime.now())
	return time

@client.event
async def on_ready():
    print('Daedalus is ready!')

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command()
async def server(ctx):
	message = 'Server is located at: {}'.format(remote)
	await ctx.send(message)

@client.command()
async def daedalus(ctx):
	logo = '''```css

      .o8                            .o8            oooo                       
     "888                           "888            `888                       
 .oooo888   .oooo.    .ooooo.   .oooo888   .oooo.    888  oooo  oooo   .oooo.o 
d88' `888  `P  )88b  d88' `88b d88' `888  `P  )88b   888  `888  `888  d88(  "8 
888   888   .oP"888  888ooo888 888   888   .oP"888   888   888   888  `"Y88b.  
888   888  d8(  888  888    .o 888   888  d8(  888   888   888   888  o.  )88b 
`Y8bod88P" `Y888""8o `Y8bod8P' `Y8bod88P" `Y888""8o o888o  `V88V"V8P' 8""888P' 

```'''
	await ctx.send(logo)

@client.command()
async def man(ctx):
	embed = discord.Embed(color = 0x6393f)
	
	embed.title = 'Commands:'
	embed.add_field(name='`ping`', value='Pong!', inline=True)
	embed.add_field(name='`daedalus`', value='Display ASCII art', inline=True)
	embed.add_field(name='`help`', value='Will display all commands and their uses', inline=False)
	embed.add_field(name='`server`', value='Will display the server the bot is currently pulling scores from', inline=False)

	embed.add_field(name='`top`', value='Will fetch the top 10 scores', inline=False)
	embed.add_field(name='`team <team_name>`', value='Will fetch score details for the team specified', inline=False)
	embed.add_field(name='`export`', value='Will fetch a file containing current scores', inline=False)
	embed.add_field(name='`scoreboard <number>`', value='Will fetch the top <number> scores. If the message is too large to be sent on discord it will be sent as a text file', inline=False)
	embed.add_field(name='`image <image_name> <number>`', value='Will fetch the top <number> scores for the image specified. If the message is too large to be sent on discord it will be sent as a text file', inline=False)
	await ctx.send(embed=embed)

@client.command()
async def top(ctx):
	data = requests.get(remote)
	content = data.content 
	soup = BeautifulSoup(content, 'html.parser')

	scores = soup.find_all('tr')
	top_comp = []
	first_message = '''  Rank   Team   Images	Time     Score'''
	for team in scores[0:10]:
		team = team.find_all('a')
		team_info = [ team[0].contents[0], team[1].contents[0], team[2].contents[0], team[3].contents[0]]
		team_info_fixed = []
		for element in team_info:
			team_info_fixed.append(element.strip())
		
		detail = '''{}	{}	{}	{}'''.format(team_info_fixed[0],team_info_fixed[1], team_info_fixed[2], team_info_fixed[3])
		top_comp.append(detail)
	
	i = 1
	new = []
	new.append(first_message)
	for lin in top_comp[0:10]:
		n = ' #{}	'.format(i)
		if len(n) < 5:
			n = '  #{}	'.format(i)
		lin = n + lin
		new.append(lin)
		i += 1

	formatted = '\n'
	formatted = formatted.join(new)
	formatted = '```' + formatted + '```'

	h_find = soup.find_all('h4')
	round_title = h_find[0].text


	embed = discord.Embed(color = 0x36393f)
	embed.title = round_title
	embed.add_field(name="Time", value=get_time(), inline=False)
	embed.description = formatted

	await ctx.send(embed=embed)

@client.command()
async def scoreboard(ctx, num):
	os.system('rm -rf scoreboard.txt')
	data = requests.get(remote)
	num = int(num)
	content = data.content 
	soup = BeautifulSoup(content, 'html.parser')

	h_find = soup.find_all('h4')
	round_title = h_find[0].text

	scores = soup.find_all('tr')
	comp = []
	first_message = '''  Rank  Team	Images Time	    Score'''
	for team in scores:
		team = team.find_all('a')
		team_info = [ team[0].contents[0], team[1].contents[0], team[2].contents[0], team[3].contents[0]]
		team_info_fixed = []
		for element in team_info:
			team_info_fixed.append(element.strip())
		
		detail = '''{}	{}	{}	{}'''.format(team_info_fixed[0],team_info_fixed[1], team_info_fixed[2], team_info_fixed[3])
		comp.append(detail)
	
	i = 1
	new = []
	new.append(first_message)
	for lin in comp[0:num]:
		n = ' #{}	'.format(i)
		if len(n) < 5:
			n = '  #{}	'.format(i)
		lin = n + lin
		new.append(lin)
		i += 1

	formatted = '\n'
	formatted_old = formatted.join(new)
	formatted = '```' + formatted_old + '```'


	h_find = soup.find_all('h4')
	round_title = h_find[0].text

	embed = discord.Embed(color = 0x36393f)
	embed.title = round_title
	embed.add_field(name="Time", value=get_time(), inline=False)
	embed.description = formatted

	try:
		await ctx.send(embed=embed)
	except:
		os.system('touch scoreboard.txt')
		fle = open('scoreboard.txt', 'w')
		fle.write(formatted_old)
		fle.close()
		await ctx.send(file=discord.File('scoreboard.txt'))

@client.command()
async def team(ctx, arg):
	global remote
	url = '{}scores/css?team={}'.format(remote, str(arg))
	team_data = requests.get(url)
	content = team_data.content
	soup = BeautifulSoup(content, 'html.parser')
	scores = soup.find_all('table', {"class": "table table-borderless table-dark table-striped"})
	
	tds = []

	for thing in scores:
		tds.append(thing.find_all('tr'))
	
	general_tags = tds[0]

	image_tags = tds[1]
	temp = []

	for gentag in general_tags:
		gentemp = gentag.find_all('td')

	for j, gentag in enumerate(gentemp):
		gentemp[j] = '`{}`'.format(gentag.text)
	
	for tag in image_tags:
		temp.append(tag.find_all('td'))

	for list in temp:
		for i, tag in enumerate(list):
			list[i] = tag.text

	report = []

	for list in temp:
		message = '''Image: {} 	Time: {} Score: ({}/{}) {}'''.format(list[0], list[1], list[2], list[3], list[4])
		report.append(message)
	
	formatted = '\n'
	formatted = formatted.join(report)
	formatted = '```' + formatted + '```'
	
	title = 'Scores for {}:'.format(arg)

	embed = discord.Embed(color = 0x36393f)
	embed.title = title
	embed.add_field(name="Elapsed Time", value=gentemp[0], inline=False)
	embed.add_field(name="Play Time", value=gentemp[1], inline=False)
	embed.add_field(name="Total Score", value=gentemp[2], inline=False)
	embed.add_field(name="Current Image Scores", value=formatted, inline=False)
	embed.add_field(name="Time", value=get_time(), inline=False)
	embed.add_field(name="Link", value=url, inline=False)

	await ctx.send(embed=embed)

@client.command()
async def export(ctx):
	os.system('rm -rf scoreboard.txt')
	data = requests.get(remote)
	content = data.content 
	soup = BeautifulSoup(content, 'html.parser')

	h_find = soup.find_all('h4')
	round_title = h_find[0].text

	scores = soup.find_all('tr')
	comp = []
	first_message = '''  Rank  Team	Images Time	    Score'''
	for team in scores:
		team = team.find_all('a')
		team_info = [ team[0].contents[0], team[1].contents[0], team[2].contents[0], team[3].contents[0]]
		team_info_fixed = []
		for element in team_info:
			team_info_fixed.append(element.strip())
		
		detail = '''{}	{}	{}	{}'''.format(team_info_fixed[0],team_info_fixed[1], team_info_fixed[2], team_info_fixed[3])
		comp.append(detail)
	
	i = 1
	new = []
	new.append(first_message)
	for lin in comp:
		n = ' #{}	'.format(i)
		if len(n) < 5:
			n = '  #{}	'.format(i)
		lin = n + lin
		new.append(lin)
		i += 1

	formatted = '\n'
	formatted_old = formatted.join(new)
	formatted = '```' + formatted_old + '```'


	h_find = soup.find_all('h4')
	round_title = h_find[0].text

	top_title = '''{} | Report Generated on {} | Server at {}'''.format(round_title, get_time(), remote)

	os.system('touch scoreboard.txt')
	fle = open('scoreboard.txt', 'w')
	fle.write(top_title)
	fle.write(formatted_old)
	fle.close()

	await ctx.send(file=discord.File('scoreboard.txt'))

@client.command()
async def image(ctx, name, num):
	os.system('rm -rf scoreboard.txt')
	num = int(num)
	url = '{}scores/css?image={}'.format(remote, str(name))
	team_image_data = requests.get(url)
	content = team_image_data.content 
	soup = BeautifulSoup(content, 'html.parser')

	h_find = soup.find_all('h4')
	round_title = h_find[0].text

	scores = soup.find_all('tr')
	comp = []
	first_message = '''  Rank  Team	Images Time	    Score'''
	for team in scores:
		team = team.find_all('a')
		team_info = [ team[0].contents[0], team[1].contents[0], team[2].contents[0], team[3].contents[0]]
		team_info_fixed = []
		for element in team_info:
			team_info_fixed.append(element.strip())
		
		detail = '''{}	{}	{}	{}'''.format(team_info_fixed[0],team_info_fixed[1], team_info_fixed[2], team_info_fixed[3])
		comp.append(detail)
	
	i = 1
	new = []
	new.append(first_message)
	for lin in comp[0:num]:
		n = ' #{}	'.format(i)
		if len(n) < 5:
			n = '  #{}	'.format(i)
		lin = n + lin
		new.append(lin)
		i += 1

	formatted = '\n'
	formatted_old = formatted.join(new)
	formatted = '```' + formatted_old + '```'


	h_find = soup.find_all('h4')
	round_title = '{} | [{}]'.format(h_find[0].text, name)

	embed = discord.Embed(color = 0x36393f)
	embed.title = round_title
	embed.add_field(name="Time", value=get_time(), inline=False)
	embed.description = formatted

	try:
		await ctx.send(embed=embed)
	except:
		os.system('touch scoreboard.txt')
		fle = open('scoreboard.txt', 'w')
		fle.write(formatted_old)
		fle.close()
		await ctx.send(file=discord.File('scoreboard.txt'))

client.run(bot_id)