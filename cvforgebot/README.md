# CV Forge Bot

Telegram бот для создания профессиональных резюме в формате PDF с использованием LaTeX.

#--В процессе доработки

## Возможности

- Интерактивное заполнение данных через Telegram
- Генерация PDF-резюме на основе шаблона Jake's Resume
- Поддержка русского языка
- Красивое форматирование с использованием LaTeX

## Требования

- Python 3.8+
- Redis
- LaTeX (texlive-full)
- Telegram Bot Token от @BotFather

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/cvforgebot.git
cd cvforgebot
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Установите LaTeX (для Ubuntu/Debian):
```bash
sudo apt-get install texlive-full
```

4. Создайте файл .env на основе .env.example и заполните необходимые переменные:
```bash
cp .env.example .env
# Отредактируйте .env и добавьте ваш BOT_TOKEN
```

5. Запустите Redis:
```bash
redis-server
```

## Запуск

```bash
python bot.py
```

## Использование

1. Найдите бота в Telegram по его имени
2. Отправьте команду /start
3. Следуйте инструкциям бота для заполнения данных
4. После заполнения всех полей, подтвердите данные
5. Получите готовое PDF-резюме

## Структура проекта

```
cvforgebot/
├── bot.py                     # Точка входа: запуск бота
├── config.py                  # Токены, пути, настройки
├── handlers/                  # Обработчики команд
├── fsm/                      # Конечные автоматы
├── templates/                # LaTeX шаблоны
├── latex/                    # Генерация PDF
├── models/                   # Pydantic модели
├── storage/                  # Хранилище данных
├── keyboards/                # Клавиатуры
└── utils/                    # Вспомогательные функции
```

## Лицензия

MIT 