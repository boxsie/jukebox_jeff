
def get_channel_from_user(bot, user):
    for g in bot.guilds:
        for c in g.voice_channels:
            for m in c.members:
                if m.id == user.id:
                    return c

    raise Exception(f'User {user.name} is not in a voice channel')


def get_channel_from_ctx(bot, ctx):
    if hasattr(ctx.message.author, 'voice') and hasattr(ctx.message.author.voice, 'channel'):
        return ctx.message.author.voice.channel

    channel = get_channel_from_user(bot=bot, user=ctx.message.author)

    if channel:
        return channel

    raise Exception(f'Unable to get voice channel from ctx {ctx.message}')


def get_channel_from_user_id(bot, user_id):
    for g in bot.guilds:
        for c in g.voice_channels:
            for m in c.members:
                if m.id == int(user_id):
                    return c

    raise Exception(f'User {user_id} is not in a voice channel')