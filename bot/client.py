from discord.ext.commands import Bot
from discord.utils import get
from discord.channel import DMChannel

from bot.voice import Voice


class BotClient(Bot):
    def __init__(self, command_prefix='!'):
        super().__init__(command_prefix=command_prefix)
        self.voice = Voice(self)


    async def on_ready(self):
        print('Jukebox jeff is ready to play sweet tunes!')


    async def on_message(self, message):
        if message.author == self.user:
            return

        await super().on_message(message)