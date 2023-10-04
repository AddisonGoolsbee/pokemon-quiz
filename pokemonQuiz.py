import random
import time
import os
import termios
import sys
import tty

GENERATION_CUTOFFS = [0, 151, 251, 386, 493, 649, 721, 809]

def get_char_input():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if char in ["\x03", "\x04"]:
        raise KeyboardInterrupt
    return char


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


def game_setup():
    selection = (
        input(
            "You are playing with the default settings. Press s to change them\nChoose a generation\nall  1  2  3  4  5  6  7\n"
        )
        .lower()
        .strip()
    )
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
        print(pokemon_range)
    except KeyboardInterrupt:
        print("\nYou're a bum")


if __name__ == "__main__":
    main()

'''
TODO

- Default game, name all pokemon in range, in order
- win screen with statistics
- only need to name first 5 letters
- symbols/spaces are optionally excluded
- don't need to press enter if correct
- any pokemon in the current set counts for the whole set
- indicator of how many you've gotten
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
- ability to see all previously named pokemon
- arrow key selection menu for start screen/settings screen
'''