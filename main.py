from telegram import Update 
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests 
import base64
from io import BytesIO

token = "8395002324:AAFLdUQWQmMpf4hj_pMD7gjITxDHW1-kuPM"
gen_ai_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent"
param = {
    "key" : "AIzaSyDbkLnETLNAtYW847SMBMIcleWGl8wJMW0"
}

def json_creator(prompt):
    json_file = {
    "contents": [
        {
        "parts": [
            {
            "text": prompt
            }
        ],
        "role": "user"
        }
    ],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"]
    }
    }
    return json_file

# Command handler for /start 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    await update.message.reply_text("Salom men rasm generatsiya qiluvchi AI man.")

# Command handler for /help command
async def help_command(update : Update, context : ContextTypes):
    await update.message.reply_text("Mavjud bot komandalari : /start, /help")

# Message handler
async def message_handler(update : Update, context : ContextTypes) :
    user_text = update.message.text 
    js_send = json_creator(user_text)
    res = requests.post(url = gen_ai_url, params = param, json = js_send).json()
    my_img = res['candidates'][0]['content']['parts'][1]['inlineData']['data']
    final_result = base64.b64decode(my_img)
    send_image = BytesIO(final_result)

    await update.message.reply_photo(photo = send_image)

if __name__ == '__main__':
    app = ApplicationBuilder().token(token = token).build()
    
    # Handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler("help", help_command))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
 
    app.run_polling()