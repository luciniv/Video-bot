import discord
from discord.ext import commands
import os
from loguru import logger

class Demos(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        description = "Demo application"

        # Create bot instance with command prefix
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents, description=description)

    # Loads cogs when bot is ready
    async def on_ready(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                # Attempt to load each cog, ignore if already loaded
                if (f'cogs.{filename[:-3]}') in self.extensions:
                    logger.info(f"Already loaded cog: {filename}")
                else: 
                    try:
                        await bot.load_extension(f'cogs.{filename[:-3]}')
                        logger.success(f"Loaded cog: {filename}")
                    except Exception as e:
                        logger.error(f"Failed to load {filename}: {e}")
bot = Demos()

# Hot-reload cogs
@bot.command(name="reload", aliases=["r"])
@commands.is_owner()
async def reload(ctx, cog: str):
    try:
        # Unload and load the cog asynchronously
        await bot.unload_extension(f'cogs.{cog}')
        await bot.load_extension(f'cogs.{cog}')

        await ctx.send(f"Cog **{cog}** has been reloaded")
        logger.success(f"Reloaded cog: {cog}.py")
    except Exception as e:
        await ctx.send(f"❌ Error reloading cog **{cog}**: {e}")
        logger.error(f"Failed to reload {cog}.py: {e}")

# Error handling for the reload command
@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        logger.info(f"Denied !reload permissions for {ctx.message.author.name}")
    else:
        logger.info(f"!reload sent an error: {error}")

# Sync slash commands
@bot.command(name="sync", aliases=["s"])
@commands.is_owner()
async def sync_commands(ctx):
    message = await ctx.send(f"Syncing global tree...")
    try:
        await bot.wait_until_ready()
        synced = await bot.tree.sync()
        logger.success(f"{bot.user.name} has been synced globally, please wait for Discord's API to update")
    except Exception as e:
        await message.edit(content=f"❌ An error has occurred: {e}")
    else: 
        await message.edit(content=f"Main tree globally synced {len(synced)} commands.") 

# Error handling for the sync command
@sync_commands.error
async def sync_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        logger.info(f"Denied !sync permissions for {ctx.message.author.name}")
    else:
        logger.info(f"!sync sent an error: {error}")

# Run the bot
bot.run('YOUR TOKEN HERE')
