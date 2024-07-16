import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command


with open(".env") as settings:
    token = settings.readline().split("TOKEN=")[-1]


bot = Bot(token)
dp = Dispatcher()




START, END = 1, 2
ATTEMPTS = 11
game_state: dict[str, int | None] = {
    "ATTEMPTS": 0,
    "NUMBER": None,
    "GAMES": 0,
    "WINS": 0,
    "LOSES": 0,
    "IS_GAME": False
}

def get_number(message: Message) -> bool:

    return game_state["IS_GAME"] and (message.text.isdigit() or (message.text[0] == '-' and message.text[1:].isdigit())) \
            and START <= int(message.text) <= END

@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.reply('Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help')

@dp.message(Command(commands=["help"]))
async def _help(message: Message):
    await message.reply(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {game_state["ATTEMPTS"]} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?')


@dp.message(Command(commands=["cancel"]))
async def cancel(message: Message):
    game_state["GAMES"] += 1
    game_state["NUMBER"] = None
    game_state["ATTEMPTS"] = 0
    game_state["IS_GAME"] = False

    await message.reply("Жаль, будем ждать Вас снова!")

@dp.message(Command(commands=["stat"]))
async def statistics(message: Message):
    await message.reply(f"Игр сыграно: {game_state["GAMES"]}\nПобед: {game_state["WINS"]}\nПоражений: {game_state["LOSES"]}\nОсталось попыток: {game_state["ATTEMPTS"]}")

@dp.message(Command(commands=["start_game"]))
async def start_game(message: Message):
    game_state["NUMBER"] = random.randint(START, END)
    game_state["ATTEMPTS"] = ATTEMPTS
    game_state["IS_GAME"] = True
    await message.reply(f"Выберете число от {START} до {END}. У Вас {ATTEMPTS} попыток")

@dp.message(get_number)
async def game(message: Message):

    if game_state["ATTEMPTS"] == 0:
        game_state["LOSES"] += 1
        game_state["GAMES"] += 1
        game_state["IS_GAME"] = False
        number = game_state["NUMBER"]
        game_state["NUMBER"] = None
        await message.reply(f"К сожалению, Вы проиграли. Задуманное число {number}")
        return

    user_number = int(message.text)

    if user_number == game_state["NUMBER"]:
        game_state["NUMBER"] = None
        game_state["GAMES"] += 1
        game_state["WINS"] += 1
        game_state["IS_GAME"] = False
        attempts = game_state["ATTEMPTS"]
        game_state["ATTEMPTS"] = 0

        await message.reply(f"Поздравляем! Тебе удалось победить за {ATTEMPTS-attempts+1} попыток. Сыграть ещё? - /start_game")
        return
    elif user_number > game_state["NUMBER"]:
        game_state["ATTEMPTS"] -= 1
        await message.reply(f"{user_number} больше загаданного числа. Попробуйте ещё")
    else:
        game_state["ATTEMPTS"] -= 1
        await message.reply(f"{user_number} меньше загаданного числа. Попробуйте ещё")



if __name__ == "__main__":
    dp.run_polling(bot)