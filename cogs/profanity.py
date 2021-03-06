from asyncio import sleep
from datetime import datetime, timedelta
from typing import Optional
from re import search

from better_profanity import profanity
from discord import Embed, Member
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions


profanity.load_censor_words_from_file("./assets/bad_words.txt")


class Profanity(Cog, name='Profanity'):
	def __init__(self, bot):
		self.bot = bot
		self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
		# links text channel ID
  		self.links_allowed = (817593711054815252,)

	@command(
     name="addprofanity",
     aliases=["addswears",
              "addcurses"])
	@has_permissions(manage_guild=True)
	async def add_profanity(self, ctx, *words):
		with open("./assets/bad_words.txt", "a", encoding="utf-8") as f:
			f.write("".join([f"{w}\n" for w in words]))

		profanity.load_censor_words_from_file("./assets/bad_words.txt")
		await ctx.send("Action complete.")

	@command(
     name="delprofanity",
     aliases=["delswears",
              "delcurses"])
	@has_permissions(manage_guild=True)
	async def remove_profanity(self, ctx, *words):
		with open("./assets/bad_words.txt", "r", encoding="utf-8") as f:
			stored = [w.strip() for w in f.readlines()]

		with open("./assets/bad_words.txt", "w", encoding="utf-8") as f:
			f.write("".join([f"{w}\n" for w in stored if w not in words]))

		profanity.load_censor_words_from_file("./assets/bad_words.txt")
		await ctx.send("Action complete.")

	@Cog.listener()
	async def on_message(self, message):
		if not message.author.bot:
			if profanity.contains_profanity(message.content):
				await message.delete()
				await message.channel.send("You can't use that word here.")

			elif message.channel.id not in self.links_allowed and search(self.url_regex, message.content):
				await message.delete()
				await message.channel.send("You can't send links in this channel.", delete_after=10)


def setup(bot):
	bot.add_cog(Profanity(bot))
