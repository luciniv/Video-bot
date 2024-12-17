import discord
from discord.ext import commands
from loguru import logger

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping the bot for a latency check
    @commands.hybrid_command(name="ping", description="Ping the bot")
    async def ping(self, ctx):
        logger.info("🟢 Function start: /ping")
        await ctx.send(f"🏓  Pong!\n\n**Latency:** {round(self.bot.latency * 1000,2)} ms")
        logger.info("🔴 Function stop: /ping")

    # Gather stats about the current server
    @commands.hybrid_command(name="stats", description="Show server statistics")
    async def stats(self, ctx):
        logger.info("🟢 Function start: /stats")
        guild = ctx.guild
        name = guild.name
        member_count = guild.member_count
        created = guild.created_at.strftime("%B %d, %Y")
        channel_count = len(guild.channels)
        role_count = len(guild.roles)
        
        embed = discord.Embed(
            title=f"Server Stats: {name}",
            timestamp=ctx.message.created_at,
            color=0xf73f3f
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Members", value=member_count, inline=True)
        embed.add_field(name="Channels", value=channel_count, inline=True)
        embed.add_field(name="Roles", value=role_count, inline=True)
        embed.add_field(name="Created On", value=created, inline=False)
        await ctx.send(embed=embed)
        logger.info("🔴 Function stop: /stats")

async def setup(bot):
    await bot.add_cog(Stats(bot))