import nextcord
from nextcord import Interaction
from nextcord.client import slash_command
from nextcord.ext import commands

from DiscordUserId import *


class SlashCommands(commands.Cog):
    def __init__(self,client):
        self.client = client

    @slash_command(name = "help", description= "Bingung yaa bingung yaaa hiii")
    async def help(self, interaction: Interaction):
        helpEmbed = nextcord.Embed(title = "Bingung yaa", colour = nextcord.Colour.magenta())
        helpEmbed.add_field(name= "/hello", value= "Special command! Gk ada yang nyapa? Mau disapa? ketik aja /hello", inline=False)
        helpEmbed.add_field(name= "!play", value= "contoh: !play surti tejo, bisa buat nambah lagu ke queue juga", inline=False)
        helpEmbed.add_field(name= "!splay", value= "sama aja, cuma muter lagu dari spotify, pake URL ya instead of judul lagu", inline=False)
        helpEmbed.add_field(name= "!pause", value= "ya buat ngepause", inline=False)
        helpEmbed.add_field(name= "!resume", value= "ya buat resume", inline=False)
        helpEmbed.add_field(name= "!queue", value= "buat nge show queue", inline=False)
        helpEmbed.add_field(name= "!nowplaying", value= "ngasih liat skarang now playing nya apa", inline=False)
        helpEmbed.add_field(name= "!loop", value= "buat enable / disable loop", inline=False)
        helpEmbed.add_field(name= "!next", value= "buat nge skip ke next song", inline=False)
        helpEmbed.add_field(name= "!stop", value= "buat nge stop lagu skalian clear queue", inline=False)
        helpEmbed.add_field(name= "!disconnect", value= "nendang bot dari voicce channel", inline=False)
        await interaction.response.send_message(embed= helpEmbed)

    @slash_command(name = "hello", description="Replies with hello")
    async def hellocommand(self, interaction: Interaction):
    
        UserID = interaction.user.id

        if UserID == kuncung_id:
            await interaction.response.send_message("Iya Master Kuncung")

        elif UserID == eric_id:
            await interaction.response.send_message("Bacot tai si eric")

        elif UserID == owen_id:
            await interaction.response.send_message("Cot wen")
        
        elif UserID == jassen_id or UserID == jassen_id2:
            await interaction.response.send_message("Bacot la sen")
        
        elif UserID == alvin_id:
            await interaction.response.send_message("Alvin : 'Nyenyenye'")
        
        elif UserID == peter_id:
            await interaction.response.send_message("Yamete kudasai peter senpai~ iaa~~")
        
        else:
            await interaction.response.send_message("Bacot")    

def setup(client):
    client.add_cog(SlashCommands(client))