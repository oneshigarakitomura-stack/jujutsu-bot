import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


import os

TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=TOKEN)
dp = Dispatcher()


characters = [
    "👊 Yuji Itadori",
    "⚡ Satoru Gojo",
    "🐺 Megumi Fushiguro",
    "🔨 Nobara Kugisaki",
    "🗡 Maki Zen'in",
    "🐍 Toge Inumaki",
    "🐼 Panda",
    "💪 Aoi Todo",
    "🏹 Noritoshi Kamo",
    "🧹 Momo Nishimiya",
    "🔫 Mai Zen'in",
    "🤖 Kokichi Muta",
    "🌸 Kasumi Miwa",
    "🕶 Kento Nanami",
    "🩺 Shoko ieiri",
    "🧸 Masamichi Yaga",
    "📋 Kiyataka Ijichi",
    "🥋 Takuma Ino",
    "🌋 Jogo",
    "🌿 Hanami",
    "🦋 Mahito",
    "👴 Yoshinobu Gakuganji",
    "💰 Mei Mei",
    "🎒 Junpei Yoshino",
    "🧠 Kenjaku",
    "👑 Ryomen Sukuna",
    "🏯 Naobito Zen'in",
    "❄️ Uraume",
    "🎯 Saki Rindo",
    "🌌 Kaito Yuki",
    "⚔️ Yuta Okkotsu",
    "🩸 Choso",
    "🌊 Miguel",
    "🖤 Suguru Geto",
    "🥷 Atsuya Kusakabe",
    "👹 Toji Fushiguro",
    "🐙 Dagon",
    "🦾 Eiji Urushi"
]


def clean_name(name):
    for x in "👊⚡🐺🔨🗡🐍🐼💪🏹🧹🔫🤖🌸🕶🩺🧸📋🥋🌋🌿🦋👴💰🎒🧠👑🏯❄️🎯🌌⚔️🩸🌊🖤🥷👹🐙🦾":
        name = name.replace(x, "")

    return name.strip().lower().replace(" ", "_").replace("'", "")


def find_images(character, color):

    name = clean_name(character)
    result = []

    if os.path.exists("images"):

        for file in os.listdir("images"):

            if file.startswith(f"{name}_{color}_") and file.endswith(".jpg"):

                result.append("images/" + file)

    return result
    
def character_menu(page=0):

    per_page = 8

    start = page * per_page
    end = start + per_page

    buttons = []

    for i, name in enumerate(characters[start:end], start):

        buttons.append([
            InlineKeyboardButton(
                text=name,
                callback_data=f"char_{i}"
            )
        ])

    if start > 0:
        buttons.append([
            InlineKeyboardButton(
                text="⬅️ قبلی",
                callback_data=f"page_{page-1}"
            )
        ])

    if end < len(characters):
        buttons.append([
            InlineKeyboardButton(
                text="بعدی ➡️",
                callback_data=f"page_{page+1}"
            )
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )



def color_menu(index):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔵 آبی",
                    callback_data=f"color_{index}_blue"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔴 قرمز",
                    callback_data=f"color_{index}_red"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟢 سبز",
                    callback_data=f"color_{index}_green"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟡 زرد",
                    callback_data=f"color_{index}_yellow"
                )
            ]
        ]
    )



def version_menu(count):

    buttons = []

    for i in range(count):

        buttons.append([
            InlineKeyboardButton(
                text=f"نسخه {i+1}",
                callback_data=f"version_{i}"
            )
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )



selected_images = {}
@dp.message(CommandStart())
async def start(message: Message):

    await message.answer(
        "🎮 انتخاب کاراکتر Jujutsu Kaisen:",
        reply_markup=character_menu()
    )



@dp.callback_query()
async def callback(call: CallbackQuery):

    data = call.data


    if data.startswith("page_"):

        page = int(data.split("_")[1])

        await call.message.edit_reply_markup(
            reply_markup=character_menu(page)
        )


    elif data.startswith("char_"):

        index = int(data.split("_")[1])

        await call.message.answer(
            f"{characters[index]}\n\n🎨 رنگ را انتخاب کن:",
            reply_markup=color_menu(index)
        )


    elif data.startswith("color_"):

        parts = data.split("_")

        index = int(parts[1])
        color = parts[2]

        images = find_images(
            characters[index],
            color
        )


        if len(images) == 0:

            await call.message.answer(
                "❌ عکس پیدا نشد"
            )


        elif len(images) == 1:

            photo = FSInputFile(images[0])

            await call.message.answer_photo(
                photo=photo
            )


        else:

            selected_images[call.from_user.id] = images

            await call.message.answer(
                "📸 نسخه را انتخاب کن:",
                reply_markup=version_menu(len(images))
            )


    elif data.startswith("version_"):

        index = int(data.split("_")[1])

        images = selected_images.get(
            call.from_user.id
        )


        if images:

            photo = FSInputFile(images[index])

            await call.message.answer_photo(
                photo=photo
            )



async def main():

    print("BOT STARTED")

    await dp.start_polling(bot)



asyncio.run(main())
