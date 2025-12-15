import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "")
WEBHOOK_SECRET_PATH = os.getenv("WEBHOOK_SECRET_PATH", "")

def require_env(name: str, value: str) -> str:
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value

def build_webhook_url(base: str, path: str) -> str:
    base = base.rstrip("/")
    path = path.lstrip("/")
    return f"{base}/{path}"

# ===== Команды бота =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🇨🇿 *Čeština s TS*\n\n"
        "Выберите, пожалуйста, нужный раздел:\n\n"
        "• Подготовка A2/B1 — /uslugi\n"
        "• Письменная подготовка (чат) — /produkty\n"
        "• Задания: письмо и устная часть — /zadani\n"
        "• Запись на экзамен — /zapis\n"
        "• Задать вопрос — /support"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def uslugi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 *Подготовка к экзамену A2/B1*\n\n"
        "Индивидуальные и групповые форматы.\n"
        "Поддержка, структура и уверенность перед экзаменом.\n\n"
        "Напишите, пожалуйста, Ваш уровень: A2 или B1.",
        parse_mode="Markdown",
    )

async def produkty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✍️ *Письменная подготовка — Telegram-чат*\n\n"
        "Закрытый чат с заданиями и проверкой.\n"
        "Материалы нельзя копировать или пересылать.\n\n"
        "Напишите, пожалуйста: A2 или B1.",
        parse_mode="Markdown",
    )

async def zadani(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧩 *Задания: письмо и устная часть*\n\n"
        "Отдельные задания для подготовки к экзамену.\n"
        "Подходит для тренировки конкретных навыков.\n\n"
        "Напишите, пожалуйста, что Вам нужно: письмо или устная часть.",
        parse_mode="Markdown",
    )

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    support_username = os.getenv("SUPPORT_USERNAME", "your_username")
    await update.message.reply_text(
        f"💬 Вы можете написать сюда:\nhttps://t.me/{support_username}\n\n"
        "Опишите, пожалуйста, Ваш уровень и цель."
    )

async def zapis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🗓 *Запись на экзамен A2/B1*\n\n"
        "Я помогу Вам разобраться с регистрацией и сроками.\n\n"
        "Напишите, пожалуйста:\n"
        "• город в Чехии\n"
        "• желаемый месяц экзамена",
        parse_mode="Markdown",
    )

# ===== Запуск =====

def main():
    token = require_env("BOT_TOKEN", BOT_TOKEN)
    base_url = require_env("PUBLIC_BASE_URL", PUBLIC_BASE_URL)
    secret_path = require_env("WEBHOOK_SECRET_PATH", WEBHOOK_SECRET_PATH)

    port = int(os.getenv("PORT", "8080"))
    webhook_url = build_webhook_url(base_url, secret_path)

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("uslugi", uslugi))
    app.add_handler(CommandHandler("produkty", produkty))
    app.add_handler(CommandHandler("zadani", zadani))
    app.add_handler(CommandHandler("support", support))
    app.add_handler(CommandHandler("zapis", zapis))

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=secret_path,
        webhook_url=webhook_url,
        allowed_updates=Update.ALL_TYPES,
    )

if __name__ == "__main__":
    main()
