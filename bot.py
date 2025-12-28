import discord
from discord.ext import commands
import json

TOKEN = ""

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)


# ---------------------------
# Yardımcı Fonksiyon
# ---------------------------
def ders_programini_yukle():
    with open("ders_programi.json", "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------
# Ders Programı Butonu
# ---------------------------
class DersProgramiButon(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="📅 Ders Programımı Göster",
        style=discord.ButtonStyle.primary
    )
    async def ders_programi(self, interaction: discord.Interaction, button: discord.ui.Button):

        program = ders_programini_yukle()

        embed = discord.Embed(
            title="📚 Haftalık Ders Programı",
            description="Aşağıda okulunuzun güncel ders programı yer almaktadır.",
            color=discord.Color.blue()
        )

        for gun, dersler in program.items():
            if not dersler:
                embed.add_field(
                    name=gun,
                    value="Bugün ders yok 🎉",
                    inline=False
                )
            else:
                ders_metni = ""
                for ders in dersler:
                    ders_metni += (
                        f"🕒 **{ders['saat']}** - {ders['ders']}\n"
                        f"👨‍🏫 {ders['egitmen']}\n\n"
                    )
                embed.add_field(
                    name=gun,
                    value=ders_metni,
                    inline=False
                )

        embed.set_footer(text="İyi dersler dileriz!")

        try:
            await interaction.user.send(embed=embed)
            await interaction.response.send_message(
                "📩 Ders programınız özel mesaj olarak gönderildi.",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Size mesaj gönderemiyorum. Lütfen DM ayarlarınızı açın.",
                ephemeral=True
            )


# ---------------------------
# Admin Komutu
# ---------------------------
@bot.tree.command(name="ders-programi", description="Ders programı butonunu gönderir (Admin)")
@commands.has_permissions(administrator=True)
async def ders_programi(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📚 Ders Programı",
        description=(
            "Ders programınızı görmek için aşağıdaki butona tıklayın.\n\n"
            "📩 Program size özel mesaj olarak gönderilecektir."
        ),
        color=discord.Color.green()
    )

    await interaction.response.send_message(
        embed=embed,
        view=DersProgramiButon()
    )


# ---------------------------
# Bot Hazır Olayı
# ---------------------------
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot giriş yaptı: {bot.user}")


bot.run(TOKEN)
