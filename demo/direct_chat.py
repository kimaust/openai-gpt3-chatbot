import time

from helpers import read_initial_prompt, read_bot_name
from chatbot import User, Bot


def main() -> None:
    initial_prompt = read_initial_prompt()

    # Add the bot name and username to the initial prompt.
    # You can remove this if you alreacy have the bot name and username in the initial prompt.
    username = input("What is your name? ")
    bot_name = read_bot_name()
    initial_prompt = f"{initial_prompt}\nYour name is {bot_name}.\nYou are talking to a person called {username}."

    user = User(username)
    bot = Bot(bot_name, initial_prompt)

    while True:
        prompt = input(f"{user.name}> ").strip()
        response = user.send_message(bot, prompt)
        print(f"{bot.name}: {response}")

        # Avoid hogging CPU too much by sleeping for one second.
        time.sleep(1)


if __name__ == "__main__":
    main()
