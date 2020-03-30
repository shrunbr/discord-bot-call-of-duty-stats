import discord
import aiohttp
from humanfriendly import format_timespan
from discord.ext import commands

#Command Category
class CallofDuty(commands.Cog):

    #Must INIT!
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()

    @commands.command()
    async def mwstats(self, ctx, platform:str, username:str, gamemode:str):
        """ Retrieve your Call of Duty MW (2019) Stats

            Platform = pc, xbox or psn
            Username= Battle.Net (PC), Xbox Gamertag (Xbox), PSN Username (PSN) 
            Gamemode = mp (Multiplayer), battle (Battle Royale) or plunder (Plunder)

            Command Example: .mwstats pc GenericUser#123 mp
        """
        platform = platform.replace("pc", "battle")
        platform = platform.replace("PC", "battle")
        platform = platform.replace("xbox", "xbl")
        platform = platform.replace("playstation", "psn")
        username = username.replace("#", "%23")
        url = "https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{}/gamer/{}/profile/type/{}".format(
            platform, username, gamemode
        )
        if gamemode == "mp":
            async with self.session.get(url) as r:
                result = await r.json()
                if r.status == 200:
                    if result["data"]:
                        embed = discord.Embed(title="Modern Warfare Stats", description=(f'Multiplayer stats for {ctx.message.author.name}'))
                        embed.add_field(name="Username", value=(result["data"]["username"]), inline=False)
                        embed.add_field(name="Level", value=(int(result["data"]["level"])), inline=False)
                        embed.add_field(name="Total Time Played", value=format_timespan(int(result["data"]["lifetime"]["all"]["properties"]["timePlayedTotal"])), inline=False)
                        embed.add_field(name="Total Kills", value=(int(result["data"]["lifetime"]["all"]["properties"]["kills"])))
                        embed.add_field(name="Total Deaths", value=(int(result["data"]["lifetime"]["all"]["properties"]["deaths"])))
                        embed.add_field(name="KDR", value=round(float(result["data"]["lifetime"]["all"]["properties"]["kdRatio"]), 2))
                        embed.add_field(name="Total Wins", value=(int(result["data"]["lifetime"]["all"]["properties"]["wins"])))
                        embed.add_field(name="Total Losses", value=(int(result["data"]["lifetime"]["all"]["properties"]["losses"])))
                        embed.add_field(name="WLR", value=round(float(result["data"]["lifetime"]["all"]["properties"]["winLossRatio"]), 2))
                        embed.add_field(name="Best Killstreak", value=(int(result["data"]["lifetime"]["all"]["properties"]["bestKillStreak"])))
                        embed.add_field(name="Best Kills (Match)", value=(int(result["data"]["lifetime"]["all"]["properties"]["bestKills"])))
                        embed.add_field(name="Best Deaths (Match)", value=(int(result["data"]["lifetime"]["all"]["properties"]["bestDeaths"])))
                        embed.set_footer(text="This data is property of Infinity Ward")
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("No results found.")
        if gamemode == "battle":
            gamemode = gamemode.replace("battle", "wz")
            async with self.session.get(url) as r:
                result = await r.json()
                if r.status == 200:
                    if result["data"]:
                        embed = discord.Embed(title="Modern Warfare Stats", description=(f'Battle Royale stats for {ctx.message.author.name}'))
                        embed.add_field(name="Username", value=(result["data"]["username"]), inline=False)
                        embed.add_field(name="Total Time Played", value=format_timespan(int(result["data"]["lifetime"]["mode"]["br"]["properties"]["timePlayed"])), inline=False)
                        embed.add_field(name="Total Games Played", value=(int(result["data"]["lifetime"]["mode"]["br"]["properties"]["gamesPlayed"])), inline=False)
                        embed.add_field(name="Total Wins", value=(int(result["data"]["lifetime"]["mode"]["br"]["properties"]["wins"])))
                        embed.add_field(name="Total Top 5s", value=(int(result["data"]["lifetime"]["mode"]["br"]["properties"]["topFive"])))
                        embed.add_field(name="Total Top 10s", value=(int(result["data"]["lifetime"]["mode"]["br"]["properties"]["topTen"])))
                        embed.add_field(name="Total Kills", value=(int(result["data"]["lifetime"]["mode"]["br"]["properties"]["kills"])))
                        embed.add_field(name="Total Deaths", value=(int(result["data"]["lifetime"]["mode"]["br"]["properties"]["deaths"])))
                        embed.add_field(name="KDR", value=round(float(result["data"]["lifetime"]["mode"]["br"]["properties"]["kdRatio"]), 2))
                        embed.set_footer(text="This data is property of Infinity Ward")
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("No results found.")
        if gamemode == "plunder":
            gamemode = gamemode.replace("plunder", "wz")
            async with self.session.get(url) as r:
                result = await r.json()
                if r.status == 200:
                    if result["data"]:
                        embed = discord.Embed(title="Modern Warfare Stats", description=(f'Plunder stats for {ctx.message.author.name}'))
                        embed.add_field(name="Username", value=(result["data"]["username"]), inline=False)
                        embed.add_field(name="Total Time Played", value=format_timespan(int(result["data"]["lifetime"]["mode"]["br_dmz"]["properties"]["timePlayed"])), inline=False)
                        embed.add_field(name="Total Games Played", value=(int(result["data"]["lifetime"]["mode"]["br_dmz"]["properties"]["gamesPlayed"])), inline=False)
                        embed.add_field(name="Total Wins", value=(int(result["data"]["lifetime"]["mode"]["br_dmz"]["properties"]["wins"])))
                        embed.add_field(name="Total Top 5s", value=(int(result["data"]["lifetime"]["mode"]["br_dmz"]["properties"]["topFive"])))
                        embed.add_field(name="Total Top 10s", value=(int(result["data"]["lifetime"]["mode"]["br_dmz"]["properties"]["topTen"])))
                        embed.add_field(name="Total Kills", value=(int(result["data"]["lifetime"]["mode"]["br_dmz"]["properties"]["kills"])))
                        embed.add_field(name="Total Deaths", value=(int(result["data"]["lifetime"]["mode"]["br_dmz"]["properties"]["deaths"])))
                        embed.add_field(name="KDR", value=round(float(result["data"]["lifetime"]["mode"]["br_dmz"]["properties"]["kdRatio"]), 2))
                        embed.set_footer(text="This data is property of Infinity Ward")
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("No results found.")


#Add cog to bot
def setup(client):
    client.add_cog(CallofDuty(client))