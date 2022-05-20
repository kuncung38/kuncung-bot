from asyncio import QueueEmpty

import os

from DiscordUserId import *

import nextcord
from nextcord import VoiceState
from nextcord import Interaction
from nextcord.ext import commands

import wavelink
from wavelink.ext import spotify

import datetime

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix= '!', intents=intents)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def reload (ctx: commands.Context):
    if ctx.author.id == kuncung_id or ctx.author.id == owen_id:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.reload_extension(f'cogs.{filename[:-3]}')
        print('Cogs Reloaded')
        return await ctx.reply('Refreshed!')
    else:
        return await ctx.reply('Siapa lu reload reload???')


@client.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
    ctx = player.ctx
    vc: player = ctx.voice_client

    if vc.loop:
        return await vc.play(track)
    
    print("Track ended, next isplaying = " ,vc.is_playing())   
    
    try:
        next_song = vc.queue.get()
        await vc.play(next_song)
        EmPlay = nextcord.Embed(title = "LANJOT! Now Playing", colour=nextcord.Colour.green())
        EmPlay.add_field(name=f"{next_song.title}", value=f"By: {next_song.author}", inline=False)
        EmPlay.add_field(name="Duration", value= f"'{str(datetime.timedelta(seconds=next_song.length))}")
        EmPlay.add_field(name="Link", value=f"Song URL: {next_song.uri}")
        await ctx.send(embed=EmPlay)
        await ctx.send(f"Now playing: {next_song.title}")
    except:
        #An exception when after the track end, the queue is now empty. If you dont do this, it will get error.
        await vc.stop()
        print("Queue Empty and stopped, isplaying = ",vc.is_playing())

    if vc.is_playing():
        await client.change_presence(status=nextcord.Status.online, 
                                            activity=nextcord.Game("music like a slave :\')"))
    else:
        await client.change_presence(status=nextcord.Status.online, 
                                            activity=nextcord.Game("Life Simulator"))

@client.command(name="Play", aliases=["Puterrr"])
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    
    if not getattr(ctx.author.voice, "channel", None):
        
        if ctx.author.id == kuncung_id:
            return await ctx.send("Masuk voice channel dulu Master Kuncung...")
        elif ctx.author.id == eric_id:
            return await ctx.send("Masuk voice channel dulu laah eric goblooooog...")
        else:    
            return await ctx.send("Masuk voice channel dulu goblok...")

    if not ctx.voice_client:
        try:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            print("Connected")
            print("voice_client = ", ctx.voice_client.channel)
                
            
        except:
           return await ctx.send("masuk voice channel dulu goblok...") 

    elif not getattr(ctx.author.voice, "channel", VoiceState) == getattr(ctx.me.voice, "channel", VoiceState):
        
        if str(getattr(ctx.me.voice, "channel", VoiceState).__class__) ==  "<class 'type'>":
        
            
            await ctx.voice_client.disconnect()
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            vc.queue.reset()
            
        else:
            return await ctx.send("Kita beda channel lah...")
        
    else:
        vc: wavelink.Player = ctx.voice_client

    print("Ready to play")
    print("isplaying = ",vc.is_playing())
    
    if vc.queue.is_empty and not vc.is_playing():
        await vc.play(search)
        await ctx.send(f"Nih '{search.title}', bener gak?")
        print(f"Now Playing '{search.title}'")
        EmPlay = nextcord.Embed(title = "Now Playing", colour=nextcord.Colour.green())
        EmPlay.add_field(name=f"{search.title}", value=f"By: {search.author}", inline=False)
        EmPlay.add_field(name="Duration", value= f"{str(datetime.timedelta(seconds=search.length))}")
        EmPlay.add_field(name="Link", value=f"[Click Me]({search.uri})")
        await ctx.send(embed=EmPlay)
        

    else:
        await vc.queue.put_wait(search)
        await ctx.send(f"Lagu '{search.title}' ditambahin ke queue")
    vc.ctx = ctx
    setattr(vc, "loop", False)


@client.command()
async def splay(ctx: commands.Context, *, search: str):
    #Play from Spotify
    if not getattr(ctx.author.voice, "channel", None):
        
        if ctx.author.id == 434378724276699147:
            return await ctx.send("Masuk voice channel dulu Master Kuncung...")
        elif ctx.author.id == 414373066521706507:
            return await ctx.send("Masuk voice channel dulu laah eric goblooooog...")
        else:    
            return await ctx.send("Masuk voice channel dulu goblok...")

    if not ctx.voice_client:
        try:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            print("Connected")
            print("isplaying = ",vc.is_playing())
                
            
        except:
           return await ctx.send("masuk voice channel dulu goblok...") 

    elif not getattr(ctx.author.voice, "channel", VoiceState) == getattr(ctx.me.voice, "channel", VoiceState):
        
        if str(getattr(ctx.me.voice, "channel", VoiceState).__class__) ==  "<class 'type'>":
        
            
            await ctx.voice_client.disconnect()
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            vc.queue.reset()
            
        else:
            return await ctx.send("Kita beda channel lah...")
        
    else:
        vc: wavelink.Player = ctx.voice_client

    print("Ready to play")
    print("isplaying = ",vc.is_playing())
    
    try:
        track = await spotify.SpotifyTrack.search(query=search, return_first = True)
    except:
        if ctx.author.id == eric_id:
            return await ctx.send("Gua maunya URL spotify nya lah ericcc, baca /help makanya goblooggg")
        else:
            return await ctx.send("Maunya URL lagu spotify nya :(")
    
    if vc.queue.is_empty and not vc.is_playing():
          
            await vc.play(track)
            await ctx.send(f"Nih '{track.title}', bener gak?")
            print(f"Now Playing '{track.title}'")
            EmPlay = nextcord.Embed(title = "Now Playing, from spotify", colour=nextcord.Colour.green())
            EmPlay.add_field(name=f"{track.title}", value=f"By: {track.author}", inline=False)
            EmPlay.add_field(name="Duration", value= f"{str(datetime.timedelta(seconds=track.length))}")
            EmPlay.add_field(name="Link", value=f"[Click Me]({track.uri})")
            return await ctx.send(embed=EmPlay)

    else:
        await vc.queue.put_wait(track)
        await ctx.send(f"Lagu '{str(track.title)}' ditambahin ke queue")
    vc.ctx = ctx
    setattr(vc, "loop", False)


@client.command()
async def pause(ctx: commands.Context):
    if not getattr(ctx.author.voice, "channel", None):
      return await ctx.send("masuk voice channel dulu goblok...")
    if not ctx.voice_client:
        return await ctx.send("gk ada musik mau pause apaan?")
    elif not getattr(ctx.author.voice, "channel", VoiceState) == getattr(ctx.me.voice, "channel", VoiceState):
        
        if str(getattr(ctx.me.voice, "channel", VoiceState).__class__) ==  "<class 'type'>":
            await ctx.voice_client.disconnect()
            vc.queue.reset()
            return await ctx.send("gk ada musik mau pause apaan?")
            
        else:
            return await ctx.send("Kita beda channel lah...")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    
    if vc.is_paused():
        await ctx.send("iya ini lagi di pause aduh")
    else:
        await vc.pause()
        await ctx.send("sip di pause dulu")
        print("Paused!, is_playing = ", vc.is_playing())


@client.command()
async def resume(ctx: commands.Context):
    if not getattr(ctx.author.voice, "channel", None):
      return await ctx.send("masuk voice channel dulu goblok...")
    if not ctx.voice_client:
        return await ctx.send("gk ada musik mau resume apaan?")
    elif not getattr(ctx.author.voice, "channel", VoiceState) == getattr(ctx.me.voice, "channel", VoiceState):
        
        if str(getattr(ctx.me.voice, "channel", VoiceState).__class__) ==  "<class 'type'>":   
            await ctx.voice_client.disconnect()
            vc.queue.reset()
            return await ctx.send("gk ada musik mau resume apaan?")
            
        else:
            return await ctx.send("Kita beda channel lah...")
    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.is_paused():
        await vc.resume()
        await ctx.send("sip lanjoooot")
    else:
        await ctx.send("Gk ada yang di pause, mau resume apaan?")

@client.command()
async def next(ctx: commands.Context):
    if not getattr(ctx.author.voice, "channel", None):
      return await ctx.send("masuk voice channel dulu goblok...")
    if not ctx.voice_client:
        return await ctx.send("gk ada musik mau next apaan?")
    elif not getattr(ctx.author.voice, "channel", VoiceState) == getattr(ctx.me.voice, "channel", VoiceState):
        
        if str(getattr(ctx.me.voice, "channel", VoiceState).__class__) ==  "<class 'type'>": 
            await ctx.voice_client.disconnect()
            vc.queue.reset()
            return await ctx.send("gk ada musik mau next apaan?")
            
        else:
            return await ctx.send("Kita beda channel lah...")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.stop()
    print("next, isplaying = ",vc.is_playing())
    if not vc.queue.is_empty:
        await ctx.send("oke di skip dulu lagu sampah")
    else:
        await ctx.send("mau nge skip lagu sampah tapi queuenya udah kosong :(")

@client.command()
async def stop(ctx: commands.Context):
    if not getattr(ctx.author.voice, "channel", None):
      return await ctx.send("masuk voice channel dulu goblok...")
    if not ctx.voice_client:
        return await ctx.send("gk ada musik mau stop apaan?")
    elif not getattr(ctx.author.voice, "channel", VoiceState) == getattr(ctx.me.voice, "channel", VoiceState):
        
        if str(getattr(ctx.me.voice, "channel", VoiceState).__class__) ==  "<class 'type'>":         
            await ctx.voice_client.disconnect()
            vc.queue.reset()
            return await ctx.send("gk ada musik mau stop apaan?")
            
        else:
            return await ctx.send("Kita beda channel lah...")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.stop()
    vc.queue.reset()
    await ctx.send("kita stop lagu lagu sampah")
    

@client.command()
async def disconnect(ctx: commands.Context):
    if not getattr(ctx.author.voice, "channel", None):
      return await ctx.send("masuk voice channel dulu goblok...")
    if not ctx.voice_client:
        return await ctx.send("w bahkan gk ada di voice channel...")
    elif not getattr(ctx.author.voice, "channel", VoiceState) == getattr(ctx.me.voice, "channel", VoiceState):
        
        if str(getattr(ctx.me.voice, "channel", VoiceState).__class__) ==  "<class 'type'>":   
            await ctx.voice_client.disconnect()
            vc.queue.reset()
            return await ctx.send("w bahkan gk ada di voice channel...")
            
        else:
            return await ctx.send("Kita beda channel lah...")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.stop()
    vc.queue.reset()
    await vc.disconnect()
    await ctx.send("bye noobs")

@client.command()
async def loop(ctx: commands.Context):
    if not getattr(ctx.author.voice, "channel", None):
      return await ctx.send("masuk voice channel dulu goblok...")
    if not ctx.voice_client:
        return await ctx.send("gk ada musik mau loop apaan?")
    elif not getattr(ctx.author.voice, "channel", VoiceState) == getattr(ctx.me.voice, "channel", VoiceState):
            
        if str(getattr(ctx.me.voice, "channel", VoiceState).__class__) ==  "<class 'type'>":    
            await ctx.voice_client.disconnect()
            vc.queue.reset()
            return await ctx.send("gk ada musik mau loop apaan?")
            
        else:
            return await ctx.send("Kita beda channel lah...")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    try:
        vc.loop ^= True
    except Exception:
        setattr(vc, "loop", False)
    
    if vc.loop:
        return await ctx.send("Loop Loop Loop Loop!")
    else:
        return await ctx.send("Ga adaa loop loop an")

@client.command()
async def nowplaying(ctx: commands.Context):
    if not getattr(ctx.author.voice, "channel", None):
      return await ctx.send("masuk voice channel dulu goblok...")
    if not ctx.voice_client:
        return await ctx.send("gk ada musik...")
    elif not getattr(ctx.author.voice, "channel", VoiceState) == getattr(ctx.me.voice, "channel", VoiceState):
        
        if str(getattr(ctx.me.voice, "channel", VoiceState).__class__) ==  "<class 'type'>":
            await ctx.voice_client.disconnect()
            vc.queue.reset()
            return await ctx.send("gk ada musik...")
            
        else:
            return await ctx.send("Kita beda channel lah...")
    else:
        vc: wavelink.Player = ctx.voice_client
    
    await ctx.send("Skarang sih lagu muter lagu ini...")
    print(f"Now Playing '{vc.track.title}'")
    EmPlay = nextcord.Embed(title = "Now Playing", colour=nextcord.Colour.green())
    EmPlay.add_field(name=f"{vc.track.title}", value=f"By: {vc.track.author}", inline=False)
    EmPlay.add_field(name="Duration", value= f"{str(datetime.timedelta(seconds=vc.track.length))}")
    EmPlay.add_field(name="Link", value=f"[Click Me]({vc.track.uri})")
    await ctx.send(embed=EmPlay)

@client.command()
async def queue(ctx: commands.Context):
    if not getattr(ctx.author.voice, "channel", None):
      return await ctx.send("masuk voice channel dulu goblok...")
    if not ctx.voice_client:
        return await ctx.send("gk ada musik mau queue apaan?")
    elif not getattr(ctx.author.voice, "channel", VoiceState) == getattr(ctx.me.voice, "channel", VoiceState):
        
        if str(getattr(ctx.me.voice, "channel", VoiceState).__class__) ==  "<class 'type'>":
            await ctx.voice_client.disconnect()
            vc.queue.reset()
            return await ctx.send("gk ada musik mau queue apaan...")
            
        else:
            return await ctx.send("Kita beda channel lah...")
    else:
        vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty:
        return await ctx.send("Queue nya kosong woi")
    
    em = nextcord.Embed(title="Queue", colour=nextcord.Colour.blue())
    queue = vc.queue.copy()
    song_count = 0
    for song in queue:
        song_count += 1
        em.add_field(name=f"Lagu nomor {song_count}", value=f"'{song.title}'", inline=False)
    
    return await ctx.send(embed=em)


client.run('OTQ5ODUwNDAwNDY5NzAwNjMw.YiQXHg.Tn_sLTIDWZMyefm9KjZQcyF-vDI')
