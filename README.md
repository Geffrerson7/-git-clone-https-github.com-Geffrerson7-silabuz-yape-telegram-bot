# VTEX-WIZARD-TELEGRAM-BOT

## Local Installation

To run this project, you'll need to add the following environment variables to your `.env` file:

`TOKEN`

`DEVELOPER_CHAT_ID`

`BOTHOST`

`DEBUG`

Clone the project

```bash
$ git clone https://github.com/Geffrerson7/vtex-wizard-telegram-bot.git
```

Navigate to the project directory

```bash
$ cd vtex-wizard-telegram-bot
```

Create a virtual environment

```sh
$ virtualenv venv
```

Activate the virtual environment

```
# windows
$ source venv/Scripts/activate
# Linux
$ source venv/bin/activate
```

Then install the required libraries:

```sh
(venv)$ pip install -r requirements.txt
```

Once all of that is done, proceed to start the app

```bash
(venv)$ python main.py
```

## Telegram bot's menu


- `/start_ean` - EAN codes generation.
- `/start_des_format` - Descriptions excel file edition.
- `/start_img` - Download images from excel file.
- `/start_format` - Format images Excel file.
- `/start_key` - Keywords generation.
- `/start_crop_image` - Crop image.
- `/cancel_ean` - Cancel EAN codes generation.
- `/cancel_des_format` - Cancel descriptions excel file edition.
- `/cancel_img` - Cancel download images from excel file.
- `/cancel_format` - Cancel format images Excel file.
- `/cancel_key` - Cancel keywords generation.
- `/cancel_crop_image` - Cancel crop image.
- `/menu` - Explanatory menu.
