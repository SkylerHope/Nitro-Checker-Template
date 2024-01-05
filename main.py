import discord
import os
import aiohttp
from dotenv import load_dotenv
#All the modules above are required

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
intents.presences = True
intents.guilds = True
intents.messages = True


bot = discord.Bot(intents = intents)

#IMPORTANT: Ignore the comment below, only for testing
#TOKEN = ''

#Bot activity
@bot.event
async def on_ready():
	await bot.change_presence(activity = discord.Game(name = "Checking on your Nitros!"))
	print("Bot {0.user} is running...".format(bot))

#Check if user has nitro command
@bot.slash_command(name = 'nitrocheck', description = 'Check if a user has real nitro or not')
async def nitrocheck(ctx: discord.ApplicationContext, user: discord.User = None):
	if user is None:
		user = ctx.author

	async with aiohttp.ClientSession() as session:
        	try:
            		headers = {
                		'Authorization': f'Bot {TOKEN}'
           	 	}

            		async with session.get(f"https://discord.com/api/v10/users/{user.id}", headers=headers) as resp:
                		if resp.status == 200:
                    			data = await resp.json()
                    			premium_type = data.get("premium_type", 0)

                    			if premium_type == 1:
                        			await ctx.send(f" The user {user.name} has Nitro Classic!")
                    			elif premium_type == 2:
                        			await ctx.send(f"The user {user.name} has Nitro!")
                    			else:
                        			await ctx.send(f"The user {user.name} does not have Nitro! :/")
                		else:
                    			await ctx.send(f"Failed to fetch user data. Status code: {resp.status}")
        	except Exception as e:
            		await ctx.send(f"An error occurred: {e}")

#Running the bot
load_dotenv
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
