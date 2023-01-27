import os


def get_data_directory_path() -> str:
    # Get the directory of the current script.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Join the path to the data directory.
    file_path = os.path.join(current_dir, "../data")

    return file_path


def read_initial_prompt() -> str:
    data_directory_path = get_data_directory_path()

    # Read the initial prompt to give to the bot.
    with open(f"{data_directory_path}/initial_prompt.txt", "r", encoding="utf-8") as f:
        initial_prompt = f.read()

    return initial_prompt.strip()


def read_bot_name() -> str:
    data_directory_path = get_data_directory_path()

    # Read the bot name.
    with open(f"{data_directory_path}/bot_name.txt", "r", encoding="utf-8") as f:
        bot_name = f.read()

    return bot_name.strip()
