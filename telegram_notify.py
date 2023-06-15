from telegram import Update,InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import subprocess

async def send_photo_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    subprocess.run(["python3","/home/cowrie/Honeypot-Monitoring-Bot/graph_output.py"])
    photo_path = "/home/cowrie/Real-time-Honeypot-Monitoring-Bot-Assistant/img/ip.png"
    chat_id = update.effective_chat.id

    with open(photo_path, "rb") as photo_file:
        await context.bot.send_photo(chat_id=chat_id, photo=InputFile(photo_file))

async def send_photo_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    subprocess.run(["python3","/home/cowrie/Honeypot-Monitoring-Bot/graph_output.py"])
    photo_path = "/home/cowrie/Real-time-Honeypot-Monitoring-Bot-Assistant/img/username.png"
    chat_id = update.effective_chat.id

    with open(photo_path, "rb") as photo_file:
        await context.bot.send_photo(chat_id=chat_id, photo=InputFile(photo_file))

async def send_photo_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    subprocess.run(["python3","/home/cowrie/Honeypot-Monitoring-Bot/graph_output.py"])
    photo_path = "/home/cowrie/Real-time-Honeypot-Monitoring-Bot-Assistant/img/password.png"
    chat_id = update.effective_chat.id

    with open(photo_path, "rb") as photo_file:
        await context.bot.send_photo(chat_id=chat_id, photo=InputFile(photo_file))

async def send_photo_user_pass(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    subprocess.run(["python3","/home/cowrie/Honeypot-Monitoring-Bot/graph_output.py"])
    photo_path = "/home/cowrie/Real-time-Honeypot-Monitoring-Bot-Assistant/img/user_pass.png"
    chat_id = update.effective_chat.id

    with open(photo_path, "rb") as photo_file:
        await context.bot.send_photo(chat_id=chat_id, photo=InputFile(photo_file))

async def send_line_chart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    subprocess.run(["python3","/home/cowrie/Honeypot-Monitoring-Bot/line_chart_output.py"])
    photo_path = "/home/cowrie/Real-time-Honeypot-Monitoring-Bot-Assistant/img/last_10_days_conn_line_chart.png"
    chat_id = update.effective_chat.id

    with open(photo_path, "rb") as photo_file:
        await context.bot.send_photo(chat_id=chat_id, photo=InputFile(photo_file))

async def send_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = "python3 /home/cowrie/Honeypot-Monitoring-Bot/text_output.py"

    result = subprocess.check_output(command, shell=True, text=True)

    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id=chat_id, text=result)

# replace your bot token
app = ApplicationBuilder().token("1111111111:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").build()

app.add_handler(CommandHandler("ip_analysis", send_photo_ip))
app.add_handler(CommandHandler("username_analysis", send_photo_username))
app.add_handler(CommandHandler("password_analysis", send_photo_password))
app.add_handler(CommandHandler("user_pass_analysis", send_photo_user_pass))
app.add_handler(CommandHandler("conn_line_chart", send_line_chart))
app.add_handler(CommandHandler("send_result", send_result))


app.run_polling()
