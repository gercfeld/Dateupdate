import os
import asyncio
from datetime import date, datetime
from zoneinfo import ZoneInfo
from telegram import Bot
from telegram.error import BadRequest

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1002886999801
CREATION_DATE = date(2025, 7, 19)
TZ = ZoneInfo("Europe/Moscow")

last_update_date = None


def days_since_creation() -> int:
    return (datetime.now(TZ).date() - CREATION_DATE).days


def build_description(days: int) -> str:
    return f"""Привет! Это канала робуксов. Тут будут проводиться розыгрыши на робуксы и звёзды.

Владелец, по всем вопросам и проблемам: @Lee_der_CEO

Отзывы: @otzivi_kanava

Каналу: {days} дней
Создан: {CREATION_DATE.strftime('%d.%m.%Y')}

За аву спасибо @PostingsLily
"""


async def update_description(bot: Bot):
    global last_update_date

    today = datetime.now(TZ).date()
    if last_update_date == today:
        return

    try:
        await bot.set_chat_description(
            chat_id=CHANNEL_ID,
            description=build_description(days_since_creation())
        )
        last_update_date = today
        print(f"[OK] Обновлено {today}")

    except BadRequest as e:
        if "not modified" in str(e):
            last_update_date = today
            print("[INFO] Описание не изменилось")
        else:
            raise


async def main():
    bot = Bot(token=BOT_TOKEN)

    print("[START]", datetime.now(TZ))

    # обновление при запуске
    await update_description(bot)

    while True:
        now = datetime.now(TZ)

        # если ровно полночь (с запасом в минуту)
        if now.hour == 0 and now.minute == 0:
            await update_description(bot)

        await asyncio.sleep(60)  # проверка раз в минуту


if __name__ == "__main__":
    asyncio.run(main())
