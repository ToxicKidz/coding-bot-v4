import discord
import re
import datetime
import asyncio
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.check
    async def helper_check(self):
        if self.guild:
            if self.guild.id == 681882711945641997:
                return True
                # if self.guild.get_role(726029173067481129) in self.author.roles:
                #     if (datetime.datetime.utcnow() - self.author.joined_at).days > 7:
                #         return True
        return False

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def helper(self, ctx, language=None):
        roles = {
            'Python': 807098700589301791,
            'JavaScript': 807098827185717299,
            'Java': 807098903127916584,
            'C++': 807098975986384947,
            'C#': 807099060883423272,
            'HTML/CSS': 807099145278062602,
            'Other': 806920884441972767
        }
        if not language:
            await ctx.send(embed=ctx.embed(title='What would you like help with?', description=f'**Options:** `{"`, `".join(roles)}`'))
            check = lambda m: m.channel == ctx.channel and m.author == ctx.author
            try:
                message = await self.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=ctx.error('Timed out!'))
            language = message.clean_content
        language.replace('py','python').replace('js','javascript').replace('cpp','c++').replace('csharp','c#').replace('html','HTML/CSS').replace('css','HTML/CSS')
        rep = {
            "Python": [
                "python", 
                'py'
            ], 
            "JavaScript": [
                "javascript", 
                'js'
            ], 
            'Java': 'java',
            'C++': [
                'cpp', 
                'c++'
            ], 
            'C#': [
                'csharp', 
                'c#'
            ], 
            'HTML/CSS': [
                'html', 
                'css', 
                'html/css'
            ],
            'Other': 'other'
        }
        items = []
        for k, v in rep.items():
            if isinstance(v, list):
                for e in v:
                    items.append((k, e))
            else:
                items.append((k, v))
        rep = dict((re.escape(v), k) for k, v in items) 
        pattern = re.compile("|".join(rep.keys()))
        language = pattern.sub(lambda m: rep[re.escape(m.group(0))], language.lower())
        if not language in roles:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=ctx.error('That is not a valid help role, please try again'))
        try:
            guild = self.bot.get_guild(681882711945641997)
            channel = guild.get_channel(814129029236916274)
            mention = guild.get_role(roles[language]).mention
        except:
            channel = self.bot.get_channel(814129029236916274)
            mention = '<@&{}>'.format(roles[language])
        message = await ctx.send(embed=ctx.embed(f'Are you sure that you want to ping for {language} help? By reacting to this message you confirm that you have read <#799527165863395338> and <#754712400757784709>, and that you will follow them. Failure to follow the help rules may result in a punishment from the moderation team. Failure to follow the how to get help may result in you not being helped.',title='Please Confirm'))
        await message.add_reaction('\U00002705')
        await message.add_reaction('\U0000274c')
        check = lambda reaction, user: str(reaction.emoji) in ['\U00002705', '\U0000274c'] and user.id == ctx.author.id
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send(embed=ctx.error('Timed out!'))
        await message.delete()
        if str(reaction.emoji) == '\U0000274c':
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=ctx.embed(title='Cancelled!'))
        await channel.send(content=mention, embed=ctx.embed('[Click Here]({0.message.jump_url}) to help {0.author.mention}'.format(ctx), title=f'{language} Help'))
        await ctx.send(embed=ctx.embed('Submitted your request for help. Please keep in mind that our helpers are human and may not be available immediately.', title='Success'))
        
def setup(bot):
    bot.add_cog(Help(bot))