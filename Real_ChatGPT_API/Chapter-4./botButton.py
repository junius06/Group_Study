import time
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, BotCommand
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

dotenv_path = '.env/dev.env'
load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Create the Application: Application 클래스를 사용하여 봇 초기화
application = Application.builder().token(BOT_TOKEN).build()

# 명령어 목록 설정
async def set_commands(application: Application):
    commands = [
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/help", description=""),
        BotCommand(command="/tasks", description="Show task buttons"),
    ]
    await application.bot.set_my_commands(commands)

# 텔레그램 라이브러리 사용할 때에는 메소드를 비동기로 호출해야 한다.
async def cmd_task_buttons(update: Update, context: CallbackContext):
    task_buttons = [[
        InlineKeyboardButton( 'Devops', callback_data="Devops" ), # InlineKeyboardButton: 버튼생성
        InlineKeyboardButton( 'Defi', callback_data="Defi" )
    ], [
        InlineKeyboardButton( 'Blockchain', callback_data="Blockchain" )
    ], [
        InlineKeyboardButton( 'Cancel', callback_data="Cancelled")
    ]]
    
    reply_markup = InlineKeyboardMarkup(task_buttons) # 메세지 레이아웃 2차원 배열
    
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Choose the team you want',
        reply_markup=reply_markup
    )
    
async def test_button(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    
    await context.bot.send_chat_action(
        chat_id=update.effective_user.id,
        action=ChatAction.TYPING
    )
    
    await context.bot.edit_message_text(
        text=f'[{data}] 작업을 완료하였습니다.',
        chat_id=query.message.chat_id,
        message_id=query.message.message_id
    )
    
# Create a command handler: CommandHandler를 사용하여 명령어 핸들러 생성
task_buttons_handler = CommandHandler('tasks', cmd_task_buttons)
callback_buttons_handler = CallbackQueryHandler(test_button)

# Add the handler to the application: 핸들러를 애플리케이션에 추가
application.add_handler(task_buttons_handler)
application.add_handler(callback_buttons_handler)

# Set commands when the bot starts
async def on_startup(application: Application):
    await set_commands(application)

application.add_startup_callback(on_startup)

# Start the application: 애플리케이션 시작
application.run_polling()