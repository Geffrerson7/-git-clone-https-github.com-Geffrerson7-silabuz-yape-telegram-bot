from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)
from common.log import logger
from bot.service import save_images_from_excel, check_excel_path, create_excel_non_working_urls

IMAGE_EXCEL_FILE, FOLDER_PATH = range(2)


async def start_download_image(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Starts the conversation and asks for the path of the folder where the images will be saved."""
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Hi {user_name}. I will hold a conversation with you. "
        "Send /cancel_img to stop talking to me.\n\n"
        "Please, send me the path of the folder where the images will be saved."
    )

    return FOLDER_PATH


async def save_image_path(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    folder_path = update.message.text
    folder_path = folder_path.replace('"', "").replace("\\", "/")
    print(folder_path)
    if not check_excel_path(folder_path):
        await update.message.reply_text("The path doesn't exist. Please, send me other path.")
        return FOLDER_PATH

    context.user_data["folder_path"] = folder_path
    await update.message.reply_text(
        "Please, send me the Excel file with image URLs of up to 20MB in size."
    )
    return IMAGE_EXCEL_FILE


async def download_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    
    if (
        update.message.effective_attachment.mime_type
        != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ):
        await update.message.reply_text("Please send an Excel file.")
        return IMAGE_EXCEL_FILE

    new_file = await update.message.effective_attachment.get_file()

    await new_file.download_to_drive("./excel-files/image/image-url.xlsx")

    logger.info("File of %s: %s", user.first_name, "image-url.xlsx")

    await update.message.reply_text("Excel file saved!")

    folder_path = context.user_data.get("folder_path")

    save_images_from_excel("./excel-files/image/image-url.xlsx", folder_path)
    create_excel_non_working_urls("./excel-files/image/image-url.xlsx", folder_path)
    
    await update.message.reply_text(
        f"The images have been converted and stored in {folder_path}\n"
        "The failed urls have been stored in failed_urls.xlsx"
    )

    return ConversationHandler.END


async def cancel_download_image(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text("Bye! I hope we can talk again some day.")

    return ConversationHandler.END


download_img_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start_img", start_download_image)],
    states={
        FOLDER_PATH: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, save_image_path),
        ],
        IMAGE_EXCEL_FILE: [
            MessageHandler(filters.ATTACHMENT, download_image),
        ],
    },
    fallbacks=[CommandHandler("cancel_img", cancel_download_image)],
)
