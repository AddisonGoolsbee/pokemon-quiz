import time
import os
import termios
import sys
import tty
import json


class Pokemon:
    def __init__(self, name, number, set):
        self.name = name
        self.number = number
        self.set = set

    def __repr__(self):
        return self.name


class Stats:
    def __init__(self):
        self.most_difficult_pokemon = ''
        self.most_difficult_pokemon_time = 0
        self.num_correct = 0
        self.num_incorrect = 0
        self.time_start = time.time()
        self.hints_used = 0
        
    def __str__(self):
        total_time = time.time() - self.time_start
        minutes, seconds = divmod(total_time, 60)
        accuracy = self.num_correct / (self.num_correct + self.num_incorrect)
        return f'Time: {int(minutes)}:{int(seconds):02}    Accuracy: {accuracy:.1%}    Hints used: {self.hints_used}    Most difficult Pokemon: {self.most_difficult_pokemon.capitalize()}'


class Game:
    GENERATION_CUTOFFS = [0, 151, 251, 386, 493, 649, 721, 809]
    less_than_5_letter_pokemon = ['abra', 'muk', 'onix', 'jynx', 'mew', 'natu', 'xatu', 'hooh', 'aron', 'uxie', 'sawk', 'axew']

    def __init__(self):
        self.current_hint = ""
        self.pokemon = self.load_data()

    def load_data(self) -> list[Pokemon]:
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        with open(current_directory + "/pokemon.json", "r") as json_file:
            data = json.load(json_file)

        res = []
        for index, pokemon in enumerate(data):
            res.append(Pokemon(pokemon["name"], index, pokemon["set"]))
        return res

    # Choose settings and pokemon listing for the next quiz
    def setup(self):
        message = "You are playing with the default settings. Press s to change them\nChoose a generation\n1  2  3  4  5  6  7 all\n"
        selection = input(message).lower().strip()
        while True:
            match selection:
                case "s" | "settings" | "setting":
                    selection = input(
                        "Settings have not been implemented yet, please choose another option\n"
                    )
                case "all" | "a" | "full":
                    return [self.GENERATION_CUTOFFS[0], self.GENERATION_CUTOFFS[-1]]
                case "1" | "2" | "3" | "4" | "5" | "6" | "7":
                    return [
                        self.GENERATION_CUTOFFS[int(selection) - 1],
                        self.GENERATION_CUTOFFS[int(selection)],
                    ]
                case _:
                    selection = input(
                        'Invalid option, please type one of the following: 1 2 3 4 5 6 7 all settings"\n'
                    )

    def run_quiz(self, pokemon_range: list):
        self.stats = Stats()

        num_pokemon = pokemon_range[1] - pokemon_range[0]
        num_correct = 0

        answered_pokemon = []

        for index, pokemon in enumerate(
            self.pokemon[pokemon_range[0] + 1 : pokemon_range[1] + 1],
            start=pokemon_range[0] + 1,
        ):
            if pokemon.name not in answered_pokemon:
                pokemon_set = self.get_pokemon_set(index)
                current_pokemon_start_time = time.time()
                while True:
                    os.system("clear")
                    self.print_listed_pokemon(answered_pokemon)
                    print(f"{num_correct}/{num_pokemon}    Accuracy: {self.stats.num_correct}/{self.stats.num_incorrect + self.stats.num_correct}")

                    if self.validate_guess(f"{index}: ", pokemon_set):
                        num_correct += len(pokemon_set)
                        answered_pokemon += pokemon_set
                        current_pokemon_duration = time.time() - current_pokemon_start_time
                        if current_pokemon_duration > self.stats.most_difficult_pokemon_time:
                            self.stats.most_difficult_pokemon = pokemon_set[0]
                            self.stats.most_difficult_pokemon_time = current_pokemon_duration
                        break

        os.system("clear")
        self.print_listed_pokemon(answered_pokemon)
        print(f"{num_correct}/{num_pokemon}")
        print("Hooray!")
        print(self.stats)

    def validate_guess(self, prompt, answers):
        if self.current_hint:
            print(f"Hint: {self.current_hint}")
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
                    input_str = input_str.lower()

                    if self.handle_hint(input_str, answers[0]):
                        return False

                    for i in answers:
                        if (len(input_str) == len(i[:5]) and input_str == i[:5]) or (
                            len(input_str) == len(GameUtils.first_5_alphanumeric(i)[:5])
                            and input_str == GameUtils.first_5_alphanumeric(i)[:5]
                        ):
                            self.current_hint = ""
                            self.stats.num_correct += 1
                            return True

                    if len(input_str) >= 5 or user_char in ["\n", "\r"] or input_str.lower() in self.less_than_5_letter_pokemon:
                        if input_str.lower() == 'mew' and 'mewtwo' in answers:
                            continue
                        self.check_if_guess_incorrect(input_str)
                        return False

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def check_if_guess_incorrect(self, input_str):
        # checks whether the guess was a typo or an actual wrong pokemon, in which case increment the num_incorrect stat
        # add check for if it was part of the previous set
        for pokemon in self.pokemon:
            if (len(input_str) == len(pokemon.name[:5]) and input_str == pokemon.name[:5]) or (
                    len(input_str) == len(GameUtils.first_5_alphanumeric(pokemon.name)[:5])
                    and input_str == GameUtils.first_5_alphanumeric(pokemon.name)[:5]
                ):
                self.stats.num_incorrect += 1
                return

    def handle_hint(self, input_str, answer):
        if len(input_str) == 5 and input_str.lower().strip() in ["help", "hint"]:
            if len(self.current_hint) < len(answer):
                if self.current_hint == '':
                    self.stats.hints_used += 1
                self.current_hint += answer[len(self.current_hint)]

    def print_listed_pokemon(self, pokemon: list):
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

    def get_pokemon_set(self, index: int):
        pokemon_set = [self.pokemon[index].name]
        if self.pokemon[index].set:
            temp_index = index + 1
            while temp_index < len(self.pokemon) and not self.pokemon[temp_index].set:
                pokemon_set.append(self.pokemon[temp_index].name)
                temp_index += 1

        # print(data)
        # num = 0
        # for i in data[::25]:
        #     print(str(num) + ": " + i["name"])
        #     num += 25
        # exit()

        return pokemon_set

    def check_if_correct(self, guess: str, pokemon_set: list):
        for name in pokemon_set:
            if guess[:5] == name[:5]:
                return True
        return False


class GameUtils:
    @staticmethod
    def first_5_alphanumeric(s):
        result = ""
        for char in s:
            if char.isalnum():
                result += char
                if len(result) == 5:
                    break
        return result


def main():
    try:
        game = Game()
        pokemon_range = game.setup()
        game.run_quiz(pokemon_range)
    except KeyboardInterrupt:
        print("\nYou're a bum")


if __name__ == "__main__":
    main()
