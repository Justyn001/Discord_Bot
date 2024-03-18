import discord
from discord import Message, Client, Intents
from dotenv import load_dotenv
import asyncio
import yt_dlp
import os

load_dotenv()
TOKEN: str = os.getenv("DISCORD_TOKEN")
class Bot:

    def __init__(self) -> None:
        self.intents: Intents = Intents.default()
        self.intents.message_content= True # NOQA
        self.client: Client = Client(intents = self.intents)

        self.responses = {'siema':'Elo żelo', 'elo żelo':'priviet marmoladki',}

        self.voice_clients = {}
        self.yt_dlp_options = {'format': 'bestaudio/best'}
        self.yt_dlp = yt_dlp.YoutubeDL(self.yt_dlp_options)

        self.ffmpeg_options = {'options':'-vn', 'executable': 'D:\\Programy\\FFMPEG\\ffmpeg-2024-03-11-git-3d1860ec8d-full_build\\bin'}


    async def send_message(self, message: Message, user_message: str):
        if user_message != '-' and user_message[0] == '-':
            user_message = user_message[1:]
            try:
                await message.channel.send(self.get_respond(user_message))
            except Exception as e:
                print(f"Error type: {e}.")
    def get_respond(self, user_message: str) -> str:
        lowered: str = user_message.lower()
        for key,value in self.responses.items():
            if lowered in key:
                return value

    async def on_message(self, message: Message):
        if message.author != self.client.user:
            author: str = str(message.author)
            content: str = str(message.content)
            channel: str = str(message.channel)

            print("{}, {}, {}".format(author,channel, message))
            await self.send_message(message, content)

    async def on_music(self, message: Message):

        try:
            voice_client = await message.author.voice.channel.connect()     # Bot wchodzi na kanał
            self.voice_clients[voice_client.guild.id] = voice_client        # Ta linia zapisuje obiekt voice_client w słowniku voice_clients.
        except Exception as e:                                              # Kluczem w słowniku jest identyfikator serwera (guild.id), aby można
            print(e)                                                        # było później odnaleźć połączenie głosowe dla danego serwera.

        url = message.content.split()[1]                                # Zapisuje do url to co jest po 'play' czyli link
        loop = asyncio.get_event_loop()                                 # zwraca pętlę zdarzeń, która jest używana do wykonywania operacji asynchronicznych w danym kontekście.
                                                                            # (nie wiem co te loop robi)
        data = await loop.run_in_executor(None, lambda: self.yt_dlp.extract_info(url, download=False))
        # Ta linia wykonuje operację pobrania informacji o pliku multimedialnym z serwisu YouTube za pomocą biblioteki youtube_dl

        song = data['url']
        player = discord.FFmpegPCMAudio(song, **self.ffmpeg_options)

        self.voice_clients[message.guild.id].play(player)



    async def on_ready(self):
        print("Im logged")

    def run(self):
        self.client.run(TOKEN)

bot = Bot()

@bot.client.event
async def on_message(message: Message):
    if message.content.startswith("-play"):
        await bot.on_music(message)
    else:
        await bot.on_message(message)
@bot.client.event
async def on_login():
    await bot.on_ready()

if __name__ == "__main__":
    bot.run()
