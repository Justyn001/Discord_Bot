from discord import Message, Client, Intents
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN: str = os.getenv("DISCORD_TOKEN")
class Bot:

    def __init__(self) -> None:
        self.intents: Intents = Intents.default()
        self.intents.message_content= True # NOQA
        self.client: Client = Client(intents = self.intents)

        self.responses = {'siema':'Elo żelo', 'elo żelo':'priviet marmoladki',
                          'moja żona jest żydówką':'Przepraszamy, bedziemy trochę ciszej...'}


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

    async def on_ready(self):
        print("Im logged")

    def run(self):
        self.client.run(TOKEN)

bot = Bot()

@bot.client.event
async def on_message(message: Message):
    await bot.on_message(message)

@bot.client.event
async def on_login():
    await bot.on_ready()

if __name__ == "__main__":
    bot.run()
