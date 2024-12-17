import discord
from discord.ext import commands
from loguru import logger
import requests
import asyncio

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Fetch a riddle from the API
    @commands.hybrid_command(name="riddle", description="Get a riddle (and its answer)")
    async def riddle(self, ctx):
        logger.info("🟢 Function start: /riddle")
        try:
            response = requests.get("https://riddles-api.vercel.app/random")
            if response.status_code == 200:
                riddle = response.json()
                riddle_question = riddle.get("riddle", "No riddle found.")
                riddle_answer = riddle.get("answer", "No answer found.")

                # Send the riddle question, wait, and then edit with the answer
                riddle_embed = discord.Embed(
                    title=f"Riddle", 
                    description=f"{riddle_question}", 
                    timestamp=ctx.message.created_at,
                    color=0xf73f3f
                    )
                riddle_message = await ctx.send(embed=riddle_embed)
                answer_embed = discord.Embed(
                    title="Answer", 
                    description=f"||{riddle_answer}||", 
                    timestamp=ctx.message.created_at,
                    color=0xf73f3f
                    )
                await asyncio.sleep(15)
                await riddle_message.reply(embed=answer_embed)
            else:
                await ctx.send("Sorry, I couldn't fetch a riddle right now. Please try again later.", ephemeral=True)
        except Exception as e:
            await ctx.send("An error occurred while fetching the riddle.")
            logger.error(f"/riddle sent an error: {e}")
        logger.info("🔴 Function stop: /riddle")

async def setup(bot):
    await bot.add_cog(Fun(bot))