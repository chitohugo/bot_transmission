import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters, \
    ContextTypes



from api_external.yts_service import YtsApi
from api_external.yts_api import YtsApiClient
from client_torrent.torrent_service import TorrentService
from client_torrent.transmission_client import TransmissionClient

load_dotenv()

HELP = """Transmission Telegram Bot
Usage:
/help - display this help
/list - retrieve list of current torrents and their status
/add <URI> - add torrent and start download 
/search <TITLE> - search by title and download
"""


class BotHandler:
    def __init__(self, menu_service, movie_service):
        self.menu_service = menu_service
        self.movie_service = movie_service

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send the main menu when the bot starts."""
        if update.message:
            await self.menu_service.show_menu(update.message)

    async def receive_input(self, update: Update, context: CallbackContext) -> None:
        """Handle user input based on the current state."""
        state = context.user_data.get("awaiting_input")
        if state == "title":
            await self.movie_service.receive_title(update.message, context)

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle button callback queries."""
        query = update.callback_query
        await query.answer()
        data = query.data
        message = query.message

        if data.startswith("add_movies_"):
            await self.movie_service.add_movies(update, context)
        elif data == "search_movie":
            context.user_data["awaiting_input"] = "title"
            if message:
                await query.edit_message_text(text="Please write the name of the movie ⌨️:")
        elif data == "list_movie":
            await self.movie_service.list_movies(message)
        elif data == "help_command":
            await self.menu_service.show_help(message)


@dataclass
class MenuService:
    async def show_menu(self, message: Update.message) -> None:
        """Send the main menu with options."""
        keyboard = [
            [
                InlineKeyboardButton("Search Movie 🔎", callback_data="search_movie"),
                InlineKeyboardButton("List Movies 📋", callback_data="list_movie"),
            ],
            [
                InlineKeyboardButton("Help", callback_data="help_command"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text("Please choose an option: ✅", reply_markup=reply_markup)

    async def show_help(self, message: Update.message) -> None:
        """Send help message."""
        await message.reply_text(HELP)
        await self.show_menu(message)


@dataclass
class MovieService:
    menu_service: MenuService
    client = TransmissionClient()
    service = TorrentService(client)

    async def add_movies(self, update: Update, context: CallbackContext) -> None:
        """Handle adding movies via callback."""
        query = update.callback_query
        await query.answer()

        movie_id = query.data.split('_')[-1]
        url = context.user_data.get(f"movie_{movie_id}")

        if url:
            torrent = self.service.add_torrent(url)
            if torrent:
                await query.message.reply_text(f"{torrent.name} added successfully ✅")
            else:
                await query.message.reply_text("Failed to add torrent ❌")
        else:
            await query.message.reply_text("URL not found ❌")
        await self.menu_service.show_menu(query.message)

    async def list_movies(self, message: Update.message) -> None:
        """List current torrents."""
        response = self.service.list_torrents()
        await message.reply_text(response, parse_mode=ParseMode.HTML)
        await self.menu_service.show_menu(message)

    async def search_movie(self, message: Update.message, context: CallbackContext) -> None:
        """Search for movies by title."""
        title = context.user_data.get("title")
        client = YtsApiClient()
        service = YtsApi(client)
        if title:
            torrents = service.search_custom(title)
            await message.reply_text("Searching for movies 🔎...")
            await self.selector_movies(message, context, torrents)
        else:
            await message.reply_text("No title provided.")

    async def selector_movies(self, message: Update.message, context: CallbackContext, torrents: List[dict]) -> None:
        """List movies with buttons to add torrents."""
        keyboard = []
        for i, item in enumerate(torrents):
            movie_id = f"movie_{i}"
            context.user_data[movie_id] = item["torrents"][0]
            keyboard.append(
                [InlineKeyboardButton(f"{item['title']} {item['year']} 🎬", callback_data=f"add_movies_{movie_id}")]
            )
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text("Please choose an title for download: 🎬", reply_markup=reply_markup)

    async def receive_title(self, message: Update.message, context: CallbackContext) -> None:
        """Handle receiving a movie title input."""
        title = message.text
        await message.reply_text(f"Looking for movie: {title}")
        context.user_data["title"] = title
        await self.search_movie(message, context)


@dataclass
class BotTransmission:
    token: str
    app: Application
    bot_handler: BotHandler

    def __init__(self, token: str):
        self.token = token
        self.app = Application.builder().token(token=self.token).build()
        menu_service = MenuService()
        movie_service = MovieService(menu_service=menu_service)
        self.bot_handler = BotHandler(menu_service=menu_service, movie_service=movie_service)
        self.add_handlers()

    def add_handlers(self):
        """Add command and callback handlers to the bot."""
        self.app.add_handler(CommandHandler("start", self.bot_handler.start))
        self.app.add_handler(CallbackQueryHandler(self.bot_handler.button))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.bot_handler.receive_input))

    def run(self):
        """Start the bot polling and print a start message."""
        print("Starting bot...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    bot = BotTransmission(os.getenv("TOKEN"))
    bot.run()
