from telegram import (
    Update,
    ReplyKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
)

from dotenv import load_dotenv
import os
import requests
import json

import api


(MENU_STATE,
 TRUCK_STATE,
) = range(2)


MAIN_MENU_KEYBOARD = ['TRUCK FILES']



async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

    await update.message.reply_text(
        text='Please choose:',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                MAIN_MENU_KEYBOARD,
            ],
            resize_keyboard=True,
            one_time_keyboard=False,
        ),
    )

    return MENU_STATE




async def get_truck_by_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text('Please enter truck name:')

    return TRUCK_STATE




async def get_truck_by_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text('Please enter truck id:')

    return TRUCK_STATE
    



async def get_truck_files(update: Update, context: ContextTypes.DEFAULT_TYPE):

    limit = int(api.get_truck_files_count())

    print('limit:', limit)

    truck_name = update.message.text

    print('truck_name:', truck_name)
    
    await update.message.reply_text('Searching...')

    data = api.get_truck_files(limit=limit)


    if data != "":
        for i in data:
            print(i)
            if i['name'] == truck_name:
                context.user_data['truck_id'] = i['id']
                break
            else:
                context.user_data['truck_id'] = ""
    else:
        context.user_data['truck_id'] = ""


    if context.user_data['truck_id'] != "":
        files = api.get_truck_files_by_id(context.user_data['truck_id'])

        if files != "":
            for i in files:
                try:
                    await update.message.reply_text(f'File: {i}')
                except Exception as e:
                    print(e)
                    await update.message.reply_text(f'Could not file: {i}')
        else:
            await update.message.reply_text(f'Could not find truck with id: {context.user_data["truck_id"]}')
    else:
        await update.message.reply_text(f'Could not find truck with name: {context.user_data["name"]}')


    return TRUCK_STATE





async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Error: {context.error}')




if __name__ == "__main__":
    load_dotenv()

    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_handler),
        ],
        states={
            MENU_STATE: [
                MessageHandler(filters.Regex('.*TRUCK FILES$'), get_truck_by_name),
            ],
            TRUCK_STATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_truck_files),
                MessageHandler(filters.Regex('.*TRUCK FILES$'), get_truck_by_name),
            ],
        },
        fallbacks=[
            CommandHandler('start', start_handler),
            MessageHandler(filters.Regex('.*TRUCK FILES$'), get_truck_files),
        ],
    )

    app.add_handler(conv_handler)

    app.add_error_handler(error_handler)

    print("Bot started...")

    app.run_polling()
