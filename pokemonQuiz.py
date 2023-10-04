# import random
# import time
# import os
# import termios
# import sys
# import tty


# def get_char_input():
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)

#     try:
#         tty.setraw(sys.stdin.fileno())
#         char = sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     if char in ["\x03", "\x04"]:
#         raise KeyboardInterrupt
#     return char


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


# def main():
#     try:
#         print("Press CTRL+C to quit")
#         mode = input("Would you like to answer with the character or with the code?\n")
#         while True:
#             if (
#                 mode.lower().strip().startswith("char")
#                 or mode.lower().strip() == "code"
#             ):
#                 mode = "code" if mode.lower().strip() == "code" else "character"
#                 run_game(mode)
#             else:
#                 mode = input('Invalid option, please type either "char" or "code"\n')
#     except KeyboardInterrupt:
#         print("\nYou're a bum")


# if __name__ == "__main__":
#     main()

