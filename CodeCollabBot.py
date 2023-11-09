import nextcord
from nextcord.ext import commands


intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", help_command=None, intents=intents)


@bot.event
async def on_ready():
    print("Bot is ready!")


"""Voice channel to select in order to create groups of 4 - maximum"""
SQUAD_VOICE_CHANNEL_ID = 761448143312519177

"""Voice channel to select in order to create groups of 2 -max"""
DUO_VOICE_CHANNEL_ID = 761448143547924530

"""Voice channel to select in order to enter solo"""
SOLO_VOICE_CHANNEL_ID = 761448143547924531

"""Category Active Now at the bottom of the server"""
ACTIVE_NOW = 1172119935225430036

user_voice_channel = {}


@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the user has connected to the specified 'Squad'/'Duo'/'Solo' voice channel
    global user_voice_channel
    squad_voice_channel = bot.get_channel(SQUAD_VOICE_CHANNEL_ID)
    duo_voice_channel = bot.get_channel(DUO_VOICE_CHANNEL_ID)
    solo_voice_channel = bot.get_channel(SOLO_VOICE_CHANNEL_ID)

    if before.channel is None and after.channel is not None:
        """Predefined category where active voice channels will be located"""
        code_collab_category = member.guild.get_channel(ACTIVE_NOW)

        # Create a new voice channel for the user based on request
        if after.channel == squad_voice_channel:
            user_voice_channel[member] = await member.guild.create_voice_channel(
                name=f"{member.display_name}",
                position=1,
                user_limit=4,
                category=code_collab_category,
            )
        elif after.channel == duo_voice_channel:
            user_voice_channel[member] = await member.guild.create_voice_channel(
                name=f"{member.display_name}",
                position=2,
                user_limit=2,
                category=code_collab_category,
            )
        elif after.channel == solo_voice_channel:
            user_voice_channel[member] = await member.guild.create_voice_channel(
                name=f"{member.display_name}",
                position=3,
                user_limit=1,
                category=code_collab_category,
            )
        # Move the user to their private voice channel with them as host
        await member.move_to(user_voice_channel[member])

        """ Delete the voice channel when the channel creator leaves it """
    elif before.channel == user_voice_channel[member] and after.channel is None:
        # Check if the user has a voice channel
        user_voice_channels = [
            channel
            for channel in member.guild.channels
            if channel.name.startswith(f"{member.display_name}")
        ]
        if user_voice_channels:
            # Destroy the user's voice channel
            await user_voice_channels[0].delete()

        """Don't let the user switch between the active voice channels directly"""
    elif before.channel is not None and after.channel in (
        squad_voice_channel,
        duo_voice_channel,
        solo_voice_channel,
    ):
        await member.move_to(before.channel)

    else:
        """Delete inactive voice channels from ACTIVE NOW category"""
        for channel in member.guild.channels:
            if channel.category_id == ACTIVE_NOW and len(channel.members) == 0:
                await channel.delete()


bot.run("MTE2MzM3ODY5MzIzODk1NjAzMg.BOT TOKEN")
