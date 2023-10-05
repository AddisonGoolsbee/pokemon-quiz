import time
import os
import termios
import sys
import tty
import json

GENERATION_CUTOFFS = [0, 151, 251, 386, 493, 649, 721, 809]

def get_input(prompt, answers):
    input_str = ""
    print(prompt, end="", flush=True)
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            user_char = sys.stdin.read(1)
            if user_char in ["\x03", "\x04"]:
                raise KeyboardInterrupt
            elif user_char in ('\x08', '\x7f'):
                if input_str:
                    input_str = input_str[:-1]
                    print('\b \b', end='', flush=True)
            else:
                print(user_char, end="", flush=True)
                input_str += user_char
                for i in answers:
                    if len(input_str) == len(i[:5]) and input_str == i[:5]:
                        return True
                if len(input_str) >= 5:
                    return False
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def print_listed_pokemon(pokemon: list):
    for i in pokemon:
        print(i, end=" ")
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
    with open("pokemon.json", "r") as json_file:
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

            if get_input(f"{index}: ", pokemon_set):
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


# def run_game(mode: str):
#     total_time = 0.0
#     num_correct = 0
#     num_questions = 0
#     os.system("clear")
#     print("Press CTRL+C at any time to quit and view your score\n")
#     try:
#         while True:
#             if mode == "character":
#                 prompt = random.sample(list(morse_code.keys()), 1)[0]
#                 answer = morse_code[prompt]
#             else:
#                 answer = random.sample(list(morse_code.keys()), 1)[0]
#                 prompt = morse_code[answer]

#             start = time.time()
#             if mode == "character":
#                 print(prompt)
#                 guess = get_char_input()
#             else:
#                 guess = input(prompt + "\n")
#             guess = guess.upper().strip()
#             end = time.time()

#             num_questions += 1
#             os.system("clear")
#             if guess == answer:
#                 num_correct += 1
#                 print(
#                     f"{guess} is correct!    Time: {end - start:0.3f}s    {num_correct}/{num_questions}\n"
#                 )
#                 total_time += end - start
#             elif guess == "":
#                 print(f"The answer was {answer}\n")
#             else:
#                 print(f"{guess} is wrong!\n")

#     except KeyboardInterrupt:
#         num_questions = max(num_questions, 1)
#         print(
#             f"\nAccuracy: {float(num_correct) / num_questions * 100:0.1f}%\nAverage Speed: {total_time / num_questions:0.3f}s"
#         )
#         exit()


# Choose settings and generation for the quiz
def game_setup():
    message = "You are playing with the default settings. Press s to change them\nChoose a generation\nall  1  2  3  4  5  6  7\n"
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
                    'Invalid option, please type one of the following: s all 1 2 3 4 5 6 7"\n'
                )


def main():
    try:
        pokemon_range = game_setup()
        run_game(pokemon_range)
    except KeyboardInterrupt:
        print("\nYou're a bum")


if __name__ == "__main__":
    main()


"""
TODO
- win screen with statistics
- symbols/spaces are optionally excluded
- skip button that tells you the answer
- hint button that gives you the first letter
- update readme
- settings menu:
    - json file storing user's default settings, gitignored
    - first 5 letters vs full name
    - symbol exclusion
    - enter/automatic
    - set skip
    - hints enabled
    - skips enabled
    - ordered or unordered
        - set must be the first one
- arrow key selection menu for start screen/settings screen
- figure out how to fix the sixth character problem: if I type bulbas, then it gets bulba and then gives me the s for the next pokemon
"""
