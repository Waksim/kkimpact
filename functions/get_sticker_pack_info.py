import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram import F

bot = Bot(token="7007119455:AAE4UpTzYztO82An8A_1r6rPEw3mWauJ2ps")   # TEST
dp = Dispatcher()

@dp.message(F.sticker)
async def cmd_start(message: types.Message):
    # await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    sticker_id = message.sticker.file_id
    # sticker_name = 'dendro_by_KKImpact_testBOT'
    sticker_name = 'dendro_by_KKImpact_testBOT'
    # sticker_pack_info = ''

    result: bool = await bot.delete_sticker_set(name=sticker_name)
    # time.sleep(10)
    stickers_arr = []
    stickers_arr.append(types.InputSticker(sticker='https://chpic.su/_data/stickers/e/emociichat/emociichat_002.webp?v=1712286303', emoji_list=['🟢']))
    # stickers_arr.append(types.InputSticker(sticker='https://chpic.su/_data/stickers/e/emociichat/emociichat_010.webp?v=1712286303', emoji_list=['🟢']))
    result: bool = await bot.create_new_sticker_set(user_id=message.from_user.id,
                                                    name=sticker_name,
                                                    title='DENDRO :: @KKimpactBOT',
                                                    stickers=stickers_arr,
                                                    sticker_format='static',
                                                    sticker_type='regular'
                                                    )

    # print(bool)

    await message.answer_sticker(sticker_id)
    await message.answer(f"ID стикера: {sticker_id}\nhttps://t.me/addstickers/{sticker_name}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())