from settings import config
from api import app
import uvicorn
from telegram import Update
from bot.ptb import ptb
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)
from bot.handlers import error_handler, text_handler, unknown_command, bad_command
from bot.commands import start, ean_number, cancel, EAN_NUMBER

conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            EAN_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, ean_number)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

def add_handlers(dp):
    dp.add_handler(CommandHandler("menu", text_handler))
    dp.add_handler(conv_handler)
    dp.add_error_handler(error_handler)
    dp.add_handler(CommandHandler("bad_command", bad_command))
    dp.add_handler(MessageHandler(filters.COMMAND, unknown_command))

add_handlers(ptb)


if __name__ == "__main__":
    if config.DEBUG == "True":
        ptb.run_polling(allowed_updates=Update.ALL_TYPES)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)


