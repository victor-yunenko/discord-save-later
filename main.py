import os

import discord
from discord import Interaction
from discord import Message
from discord.ui import View


intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True


class MyClient(discord.Client):
    async def on_ready(self) -> None:
        pass

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        if payload.emoji.name == "💾":
            channel = await self.fetch_channel(payload.channel_id)
            message: Message = await channel.fetch_message(payload.message_id)
            user = await self.fetch_user(payload.user_id)
            embed = discord.Embed(description=message.content)
            avatar_url = (
                message.author.avatar.url
                if message.author.avatar
                else message.author.default_avatar.url
            )
            embed.set_author(name=message.author.display_name, icon_url=avatar_url)
            embed.add_field(
                name="Original Message",
                value=f"https://discord.com/channels/{message.guild.id}/{channel.id}/{message.id}",
            )
            await user.send(embed=embed, view=DeleteView())
        else:
            channel = await self.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if message.author == self.user:
                await message.delete()


class DeleteView(View):
    async def interaction_check(self, interaction: Interaction) -> bool:
        return True

    @discord.ui.button(label="Complete", style=discord.ButtonStyle.primary, custom_id="complete")
    async def delete_button(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.message.delete()


client = MyClient(intents=intents)
client.run(os.environ.get("DISCORD_TOKEN"))
