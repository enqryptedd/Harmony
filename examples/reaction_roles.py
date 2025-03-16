
import harmony

bot = harmony.Bot(command_prefix="!", intents=harmony.Intents.all())

@bot.command()
async def setup_roles(message):
    embed = harmony.embeds.EmbedBuilder() \
        .set_title("Choose your roles") \
        .set_description("React to get a role") \
        .add_field("🔴", "Red Team", True) \
        .add_field("🔵", "Blue Team", True) \
        .add_field("🟢", "Green Team", True) \
        .build()
    
    role_msg = await message.channel.send(embed=embed)
    
    await role_msg.add_reaction("🔴")
    await role_msg.add_reaction("🔵")
    await role_msg.add_reaction("🟢")

@bot.event
async def reaction_add(reaction, user):
    if user.bot:
        return
        
    if reaction.emoji == "🔴":
        # Get Red Team role and add it to user
        role = reaction.message.guild.get_role("red_role_id")
        await reaction.message.guild.add_role_to_member(user.id, role.id)
    elif reaction.emoji == "🔵":
        # Get Blue Team role and add it to user
        role = reaction.message.guild.get_role("blue_role_id")
        await reaction.message.guild.add_role_to_member(user.id, role.id)
    elif reaction.emoji == "🟢":
        # Get Green Team role and add it to user
        role = reaction.message.guild.get_role("green_role_id")
        await reaction.message.guild.add_role_to_member(user.id, role.id)

if __name__ == "__main__":
    bot.run("YOUR_TOKEN_HERE")
