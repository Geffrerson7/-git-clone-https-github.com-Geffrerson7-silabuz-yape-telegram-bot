from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from telegram import ReplyKeyboardMarkup
from settings import config
import traceback
import html
import json
from telegram.constants import ParseMode
from common.log import logger
from telegram.error import RetryAfter, BadRequest


DEVELOPER_CHAT_ID = config.DEVELOPER_CHAT_ID


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_name = update.effective_user.first_name
    message_text = f"Hello {user_name}, I'm Yape Bot!\n"
    message_text += "Here's an explanatory menu:\n\n"
    message_text += "/start - Start the conversation with the bot.\n"

    keyboard = [["/start"]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )

    await update.message.reply_text(message_text, reply_markup=reply_markup)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Limitar la longitud del mensaje si es demasiado largo
    max_message_length = 4000

    try:
        logger.error("Exception while handling an update:", exc_info=context.error)

        tb_list = traceback.format_exception(
            None, context.error, context.error.__traceback__
        )
        tb_string = "".join(tb_list)

        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        message = (
            "An exception was raised while handling an update\n"
            f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
            "</pre>\n\n"
            f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
            f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
            f"<pre>{html.escape(tb_string)}</pre>"
        )

        if len(message) > max_message_length:
            message = (
                message[:max_message_length]
                + " [...Mensaje truncado debido a la longitud...]"
            )

        await context.bot.send_message(
            chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
        )
        
        await update.message.reply_text(f"Hubo un error {type(context.error).__name__}. Por favor, inténtalo de nuevo.")
            
    except Exception as e:
        print(f"Error en error_handler(): {e}")


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = f"Sorry, the entered command is not valid.\n"
    message_text += "Here is the list of valid commands:\n\n"
    message_text += "/start - Start the conversation with the bot.\n"
    message_text += "/menu - Explanatory menu.\n"
    await update.message.reply_text(message_text)

async def bad_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Raise an error to trigger the error handler."""
    await context.bot.wrong_method_name() 