from webbrowser import get
import nextcord
from nextcord.ext import commands

import wavelink
from wavelink.ext import spotify

class OnReady(commands.Cog):
    def __init__(self, client):
        self.client = client
      

    @commands.Cog.listener()
    async def on_ready(self):
        
        await self.client.change_presence(status=nextcord.Status.online, 
                                          activity=nextcord.Game("Life Simulator"))

        self.client.loop.create_task(self.node_connect())
    
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node:wavelink.Node):
        print(f"Node {node.identifier} is ready")
        print ("Bot is ready to use")

    @commands.Cog.listener()
    async def node_connect(self):
        await self.client.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.client, host='node01.marshalxp.xyz', port=443, password='marshal', https=True, 
                                            spotify_client=spotify.SpotifyClient(
                                            client_id="c4b2ef8bb883486085afae13173b89f7", 
                                            client_secret="569877bf68ae4d5e8c401d4db1c35681")
                                            )
        #await wavelink.NodePool.create_node(bot= client, host='lavalinkinc.ml', port=443, password='incognito', https=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot and before.channel is None and after.channel is not None:
            print("Bot Joined Channel")
            await self.client.change_presence(status=nextcord.Status.online, 
                                        activity=nextcord.Game("music like a slave :\')"))
        if member.bot and before.channel is not None and after.channel is None:
            print("Bot Left the channel")
            await self.client.change_presence(status=nextcord.Status.online, 
                                            activity=nextcord.Game("Life Simulator"))

def setup(client):
    client.add_cog(OnReady(client))