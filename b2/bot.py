import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from rapidfuzz import process, fuzz

BOT_TOKEN = "8563496312:AAGuNGIovRK-XHqAUuRo_r3G_uKsMUP2vVI"
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def clean_name(name: str) -> str:
    name = name.strip()
    name = " ".join(name.split())
    return name

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! ابعت الاسم وهجبلك الرقم ورقم اللجنة.")

async def search_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = clean_name(update.message.text)
    data = load_data()

    names_list = list(data.keys())

    # البحث بنسبة تطابق 50٪
    best_match = process.extractOne(user_input, names_list, scorer=fuzz.ratio)
    
    if best_match and best_match[1] >= 50:  # نسبة التطابق 50% أو أكثر
        matched_name = best_match[0]
        number = data[matched_name].get("number", "غير متوفر")
        committee = data[matched_name].get("committee", "غير متوفر")
        reply = f"الاسم: {matched_name}\nالرقم الانتخابي: {number}\nرقم اللجنة: {committee}"
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text("الاسم غير موجود.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_name))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
