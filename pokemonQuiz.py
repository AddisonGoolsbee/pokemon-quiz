import time
import os
import termios
import sys
import tty
import json

GENERATION_CUTOFFS = [0, 151, 251, 386, 493, 649, 721, 809]

current_hint = ''


def first_5_alphanumeric(s):
    result = ""
    for char in s:
        if char.isalnum():
            result += char
            if len(result) == 5:
                break
    return result

def handle_hint(input_str, answer):
    global current_hint
    if len(input_str) == 5 and input_str.lower().strip() in ['help', 'hint']:
        if (len(current_hint) < len(answer)):
            current_hint += answer[len(current_hint)]


def validate_guess(prompt, answers):
    global current_hint
    if current_hint:
        print(f'Hint: {current_hint}')
    print(prompt, end="", flush=True)

    input_str = ""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            user_char = sys.stdin.read(1)
            # key is ^C or ^D
            if user_char in ["\x03", "\x04"]:
                raise KeyboardInterrupt
            # key is delete
            elif user_char in ("\x08", "\x7f"):
                if input_str:
                    input_str = input_str[:-1]
                    print("\b \b", end="", flush=True)
            # normal key
            else:
                print(user_char, end="", flush=True)
                input_str += user_char

                if handle_hint(input_str, answers[0]):
                    return False

                for i in answers:
                    if (len(input_str) == len(i[:5]) and input_str == i[:5]) or (
                        len(input_str) == len(first_5_alphanumeric(i)[:5])
                        and input_str == first_5_alphanumeric(i)[:5]
                    ):
                        current_hint = ''
                        return True
                    
                if len(input_str) >= 5 or user_char in ['\n', '\r']:
                    return False

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def print_listed_pokemon(pokemon: list):
    terminal_width = os.get_terminal_size().columns
    current_line_length = 0

    for poke in pokemon:
        poke_length = len(poke) + 1  # +1 for space
        if current_line_length + poke_length > terminal_width:
            print()
            current_line_length = 0

        print(poke, end=" ")
        current_line_length += poke_length

    print()


def get_pokemon_set(index: int, data: list):
    pokemon_set = [data[index]["name"]]
    if data[index]["set"]:
        temp_index = index + 1
        while temp_index < len(data) and not data[temp_index]["set"]:
            pokemon_set.append(data[temp_index]["name"])
            temp_index += 1
    return pokemon_set


def check_if_correct(guess: str, pokemon_set: list):
    for name in pokemon_set:
        if guess[:5] == name[:5]:
            return True
    return False


def run_game(range: list):
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    with open(current_directory + "/pokemon.json", "r") as json_file:
        data = json.load(json_file)

    num_pokemon = range[1] - range[0]
    num_correct = 0
    start = time.time()

    listed_pokemon = []

    for index, item in enumerate(data[range[0] + 1 : range[1] + 1], start=range[0] + 1):
        skip = True
        if item["name"] in listed_pokemon:
            skip = False

        pokemon_set = get_pokemon_set(index, data)
        while skip:
            os.system("clear")
            print_listed_pokemon(listed_pokemon)
            print(f"{num_correct}/{num_pokemon}")

            if validate_guess(f"{index}: ", pokemon_set):
                num_correct += len(pokemon_set)
                listed_pokemon += pokemon_set
                break

    os.system("clear")
    print_listed_pokemon(listed_pokemon)
    print(f"{num_correct}/{num_pokemon}")
    print("Hooray!")

    total_time = time.time() - start
    minutes, seconds = divmod(total_time, 60)
    print(f"Time: {int(minutes)}:{int(seconds):02}")


# Choose settings and generation for the quiz
def game_setup():
    message = "You are playing with the default settings. Press s to change them\nChoose a generation\n1  2  3  4  5  6  7 all\n"
    selection = input(message).lower().strip()
    while True:
        match selection:
            case "s" | "settings" | "setting":
                selection = input(
                    "Settings have not been implemented yet, please choose another option\n"
                )
            case "all" | "a" | "full":
                return [GENERATION_CUTOFFS[0], GENERATION_CUTOFFS[-1]]
            case "1" | "2" | "3" | "4" | "5" | "6" | "7":
                return [
                    GENERATION_CUTOFFS[int(selection) - 1],
                    GENERATION_CUTOFFS[int(selection)],
                ]
            case _:
                selection = input(
                    'Invalid option, please type one of the following: 1 2 3 4 5 6 7 all settings"\n'
                )


def main():
    try:
        pokemon_range = game_setup()
        run_game(pokemon_range)
    except KeyboardInterrupt:
        print("\nYou're a bum")


if __name__ == "__main__":
    main()
