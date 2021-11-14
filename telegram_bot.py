from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)


class AutoCompleteTelegramBot:
    def __init__(self, bot_token, autocompleter):
        self.bot_token = bot_token
        self.autocompleter = autocompleter
        self.updater = None
        self.dispatcher = None
        self.init_bot()
        self.init_commands()

    def init_bot(self):
        self.updater = Updater(token=self.bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
    
    def init_commands(self):
        start_handler = CommandHandler('start', self.start_reply)
        self.dispatcher.add_handler(start_handler)

        message_handler = MessageHandler(Filters.text & (~Filters.command), self.reply)
        self.dispatcher.add_handler(message_handler)

    def reply(self, update: Update, context: CallbackContext):
        query = update.message.text
        proposals = self.autocompleter.query(query, max_n=10)
        result_msg = f"Result for query: {query}\n"
        for proposal in proposals:
            proposal_message = f"Proposal: {proposal.words}. Score: {proposal.popularity}\n"
            result_msg += proposal_message

        context.bot.send_message(chat_id=update.effective_chat.id, text=result_msg)


    def start(self):
        self.updater.start_polling()

    def start_reply(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I'm autocompleter wildberries bot. Please provide query in chat and I'll try to complete it",
        )

    # def


if __name__ == "__main__":
    telegram_bot = AutoCompleteTelegramBot("2143761918:AAEX0F1QS_N3AkJPaH7LkPI7yjkpoYv_AVE")
    telegram_bot.start()
