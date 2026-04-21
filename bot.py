import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# ====== ENVIRONMENT VARIABLES ======
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# ====== START COMMAND ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Hello! I am your AI assistant. Ask me anything!")

# ====== CHAT HANDLER ======
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print("User:", user_text)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.choices[0].message.content

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=reply
        )

    except Exception as e:
        print("Error:", e)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Error occurred: " + str(e)
        )

# ====== MAIN APP ======
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
