
import harmony

bot = harmony.Bot(command_prefix="!", intents=harmony.Intents.all())

@bot.command()
async def buttons(message):
    action_row = harmony.ui.ActionRow()
    action_row.add_component(harmony.ui.Button.primary("btn_1", "Click Me"))
    action_row.add_component(harmony.ui.Button.success("btn_2", "Success"))
    action_row.add_component(harmony.ui.Button.danger("btn_3", "Danger"))
    
    await message.reply("Button Example", components=[action_row.to_dict()])

@bot.event
async def component_interaction(ctx, custom_id, component_type):
    await ctx.reply(f"Button {custom_id} was clicked!", ephemeral=True)

if __name__ == "__main__":
    bot.run("YOUR_TOKEN_HERE")
