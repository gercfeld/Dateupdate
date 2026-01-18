import os
import asyncio
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from telegram import Bot
from telegram.error import BadRequest

# === НАСТРОЙКИ ===
BOT_TOKEN = os.getenv("BOT_TOKEN")  # или впиши токен строкой
CHANNEL_ID = -1002886999801
CREATION_DATE = date(2025, 7, 19)
TZ = ZoneInfo("Europe/Moscow")
# =================


def days_since_creation() -> int:
    today_msk = datetime.now(TZ).date()
    return (today_msk - CREATION_DATE).days


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
    text = build_description(days)

    try:
        await bot.set_chat_description(
            chat_id=CHANNEL_ID,
            description=text
        )
        print(f"[OK] Описание обновлено: {days} дней")

    except BadRequest as e:
        # Telegram кидает эту ошибку, если текст не изменился
        if "not modified" in str(e):
            print("[INFO] Описание не изменилось, пропускаем")
        else:
            raise  # все остальные ошибки считаем критичными


def seconds_until_midnight_msk() -> int:
    now = datetime.now(TZ)
    tomorrow = (now + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return int((tomorrow - now).total_seconds())


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не задан")

    bot = Bot(token=BOT_TOKEN)

    print("[START] Бот запущен")
    print("[TIME] Текущее время МСК:", datetime.now(TZ))

    # Обновляем сразу при старте
    await update_description(bot)

    while True:
        wait_seconds = seconds_until_midnight_msk()
        print(f"[WAIT] Следующее обновление через {wait_seconds} сек. (00:00 МСК)")

        await asyncio.sleep(wait_seconds)

        try:
            await update_description(bot)
        except Exception as e:
            print("[ERROR]", e)


if __name__ == "__main__":
    asyncio.run(main())

