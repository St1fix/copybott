import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# Настройки из секретов GitHub
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
SESSION_STR = os.environ['SESSION_STR']
# Каналы-доноры (через запятую в секретах, например: @channel1, @channel2)
SOURCE_CHANNELS = [s.strip() for s in os.environ['SOURCE_CHANNELS'].split(',')]
# Твой канал (куда постить)
TARGET_CHANNEL = os.environ['TARGET_CHANNEL']

async def main():
    # Подключаемся через StringSession (без файлов)
    async with TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH) as client:
        for source in SOURCE_CHANNELS:
            try:
                # Берем только 1 последний пост
                async for message in client.iter_messages(source, limit=1):
                    # Пропускаем сервисные сообщения
                    if not (message.text or message.media):
                        continue
                    
                    # Простая проверка: если пост уже был переслан, Telethon это поймет
                    # Для надежности можно хранить ID последних постов в файле, 
                    # но для начала просто копируем
                    await client.send_message(TARGET_CHANNEL, message)
                    print(f"Пост из {source} успешно скопирован.")
            except Exception as e:
                print(f"Ошибка с каналом {source}: {e}")

if __name__ == '__main__':
    asyncio.run(main())
