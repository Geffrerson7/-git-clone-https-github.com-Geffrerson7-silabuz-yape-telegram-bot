from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)
from common.log import logger


EXCEL_FILE = range(1)


async def start_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks excel file with description."""
    await update.message.reply_text(
        "Hi! My name is Gef Bot. I will hold a conversation with you. "
        "Send /cancel_des to stop talking to me.\n\n"
        "Please, send me the Excel file with descriptions."
    )

    return EXCEL_FILE


async def excel_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    new_file = await update.message.effective_attachment.get_file()
    await new_file.download_to_drive("./excel-files/descriptions/description-html.xlsx")
    await update.message.reply_text("Excel file saved!")
    return ConversationHandler.END


async def cancel_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text("Bye! I hope we can talk again some day.")

    return ConversationHandler.END


description_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start_des", start_description)],
    states={
        EXCEL_FILE: [MessageHandler(filters.ATTACHMENT, excel_file)],
    },
    fallbacks=[CommandHandler("cancel_des", cancel_description)],
)
