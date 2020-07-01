import discord
from discord.ext import commands,tasks
from itertools import cycle
import youtube_dl
from discord.utils import get
import os
import random
import time

def read_token():
    with open("Token.txt" , "r") as t:
        lines = t.readlines()
        return lines[0].strip()

msg = """```\nKomutlar :\n ?spoiler - SÜRPRİZ \n ?avatar @birinietiketle -Etiketlediğin kişinin avatarı gözükür \n ?merhaba - Size Merhaba Der \n 
SESLİ KANAL KOMUTLARI \n ?join - Öncelikle sesli kanala çağırın \n ?leave - Sesli kanaldan ayrılır \n ?play url - url kısmına şarkının urlsini giriniz youtube olsun \n ?pause - Şarkıyı durdurur \n
?stop - şarkıyı kapatır \n?que - ?playde koyduğunuz şarkıyı birinci sıraya ekleyin sonra diğer şarkılarıda ekleyin sıraya eklenmiş olacak hepsi \n ?resume - durduğunuz şarkıyı devam ettirir```"""
spoiarr = ["Naruto kyuubiyi kontrol ediyor" , "Ben ölüyüm" , "Scofield ölüp diriliyor","Iron Man ölüyor" , "TOKYO GHOUL 3. SEZONDA BOZUYOR!"]
token = read_token()
client = commands.Bot(command_prefix = "?")
status = cycle(['Cooks Meth!' , '-yardım komutu ile komutları öğrenebilirsiniz' ,'Senseim Venooxa teşekkürler!'])
@client.event
async def  on_ready():
    await client.change_presence(status = discord.Status.idle , activity = discord.Game('?yardım komutuyla bilgi alabilirsiniz!'))
@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send_message(f"""Hoşgeldin {member.mention} sende artık bizdensin!""")

#commands

@client.command(name = 'merhaba' , aliases = ['Merhaba' , 'MERHABA','mrb'])
async def merhaba(ctx):
   await ctx.channel.send("Merhaba Efendim")
@client.command(name = 'yardim' , aliases = ['yardım'])
async def yardim(ctx):
    await ctx.channel.send(msg)
@client.command(name = 'spoiler' , aliases = ['spoi'])
async def spoiler(ctx):
    await ctx.channel.send(random.choice(spoiarr))
@client.command(name = 'avatar')
async def avatar(ctx, member: discord.Member):
    show_avatar = discord.Embed(
        color = discord.Color.dark_blue()
    )
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed = show_avatar)

@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"Buraya katıldım {channel}\n")

    await ctx.send(f"Sonunda bir insan ile konuşacağım {channel}")

@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Bot ayrıldı {channel}")
        await ctx.send(f"Burdan ayrıldım {channel}")
    else:
        print("Bot aslında ses kanalında değildi")
        await ctx.send("Ses kanalında yokum ama sen bilirsin")

@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("Bir şarkı yok")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Şarkı bitti sıradaki şarkı gelsin")
                print(f"Şarkı hala sırada: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("Son şarkıdan önce hiçbir şarkı sıraya alınmadı!\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Eski şarkı kaldırıldı")
    except PermissionError:
        print("Şarkı çaldığı için çıkarılamaz")
        await ctx.send("HOOP Şarkı hala çalıyor kaldıramassın")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Eski şarkı sıradan kaldırıldı")
            shutil.rmtree(Queue_folder)
    except:
        print("Sırada şarkı yok")

    await ctx.send("Şu an her şey hazır")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Şarkı şu an indiriliyor\n")
            ydl.download([url])
    except:
        print("Youtubeda böyle bir url yok acaba yanlışın mı var?")
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + c_path + '"' + " -s " + url)  # make sure there are spaces in the -s

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Tekrar adlandırıldı: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Şu an çalıyor: {nname[0]}")
    print("Çalıyor\n")

@client.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Müzik durduruldu")
        voice.pause()
        await ctx.send("Müziği durdurdun doğru mu?")
    else:
        print("Müzik çalmıyor")
        await ctx.send("Müzik yok ki durdurasın!")
@client.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Devam ediyor")
        voice.resume()
        await ctx.send("Müzik devam ediyor hazır ol")
    else:
        print("Müzik durdurulmadı ki")
        await ctx.send("Durdurulmuş bir müzik yok hatan var!")
@client.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    if voice and voice.is_playing():
        print("Müzik durduruldu")
        voice.stop()
        await ctx.send("Bitti Müzik sıradaki!")
    else:
        print("Müzik yok ki bitiresin")
        await ctx.send("Müzik olmadığı için durduramadım üzgünüm dostum")
queues = {}

@client.command(pass_context=True, aliases=['q', 'que'])
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Şarkı indiriliyor\n")
            ydl.download([url])
    except:
        print("Bu youtube linki değil üzgünüm")
        q_path = os.path.abspath(os.path.realpath("Queue"))
        system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)

    await ctx.send("Bu şarkıyı " + str(q_num) + " sıraya ekledin tebrikler!")

    print("Şarkı sıraya eklendi\n")
@client.command(pass_context=True, aliases=['n', 'nex'])
async def next(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playing Next Song")
        voice.stop()
        await ctx.send("Sıradaki şarkımız geliyorrr")
    else:
        print("No music playing")
        await ctx.send("Şarkı bitti bu kadar")

client.run(token)