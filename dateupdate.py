import os
import asyncio
from datetime import date, datetime, timedelta
from telegram import Bot

# === НАСТРОЙКИ ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1002886999801
CREATION_DATE = date(2025, 7, 19)
# =================

def days_since_creation() -> int:
    return (date.today() - CREATION_DATE).days


def build_description(days: int) -> str:
    return f"""Привет! Это канала робуксов. Тут будут проводиться розыгрыши на робуксы и звёзды.

Владелец, по всем вопросам и проблемам: @Lee_der_CEO

Отзывы: @otzivi_kanava

Каналу: {days} дней
Создан: {CREATION_DATE.strftime('%d.%m.%Y')}

За аву спасибо @PostingsLily
"""


async def update_description(bot: Bot):
    days = days_since_creation()

    await bot.set_chat_description(
        chat_id=CHANNEL_ID,
        description=build_description(days)
    )

    print(f"[OK] Обновлено: {days} дней")


def seconds_until_midnight() -> int:
    now = datetime.now()
    tomorrow = (now + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return int((tomorrow - now).total_seconds())


async def main():
    bot = Bot(token=BOT_TOKEN)

    # Обновление сразу при запуске
    await update_description(bot)

    while True:
        wait_seconds = seconds_until_midnight()
        print(f"[INFO] Следующее обновление через {wait_seconds} сек.")

        await asyncio.sleep(wait_seconds)

        try:
            await update_description(bot)
        except Exception as e:
            print("[ERROR]", e)

        await asyncio.sleep(60 * 60 * 24)


if __name__ == "__main__":
    asyncio.run(main())

