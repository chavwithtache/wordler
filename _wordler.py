import random
import json
from datetime import date
from dataclasses import dataclass
from pathlib import Path


class Wordler(object):
    def __init__(self):
        self.result_words = None
        self.allowed_words = None
        self.words_left = None
        self.result_word = None
        self.pin = None
        self.letters = None
        self.letters_in_word = 5

    @dataclass
    class Letters:
        alphabet: str = 'abcdefghijklmnopqrstuvwxyz'.upper()
        black_letters: str = ''
        yellow_letters: str = ''
        green_letters: str = ''

    def reset_all(self, letters_in_word:int = 5, result_word: str = None):
        with open(f'{Path(__file__).parent}/result_words_{letters_in_word}.json', 'r') as f:
            self.result_words = json.load(f)
        with open(f'{Path(__file__).parent}/allowed_words_{letters_in_word}.json', 'r') as f:
            self.allowed_words = json.load(f)
        self.letters_in_word= int(letters_in_word)
        self.words_left = [w for w in self.result_words]
        if result_word is not None and result_word not in self.result_words:
            raise ValueError(f'word "{result_word}" is not in the allowed list of result words.')
        self.result_word = result_word if result_word is not None else random.choice(self.result_words)
        self.pin = self.get_pin_from_result_word(self.result_word)
        self.letters = self.Letters()

    def get_help_letter(self):
        pass

    def set_and_return_words_and_scores(self, pin, words: list):
        self.reset_from_pin(pin)
        return {word.upper(): self.guess(word.lower()) for word in words}

    def reset_from_pin(self, pin):
        # TODO Improve this. Make pin cleverer
        if len(pin) == 5:
            self.letters_in_word = 7
        elif len(pin) == 3:
            self.letters_in_word = 3
        else:
            self.letters_in_word = 5

        self.reset_all(self.letters_in_word)
        self.pin = pin
        self.result_word = self.get_result_word_from_pin()
        self.words_left = [w for w in self.result_words]

    # def helper(self):
    #     print('\x1B[1;32;40myou can type EXIT to quit\x1B[0m\n')
    #
    #     while len(self.words_left) > 0:
    #         help_words = self.get_valid_help_string()
    #         if help_words is None:
    #             print('ok bye..')
    #             return
    #         word, result = help_words
    #         self.words_left = self.check(word, result)
    #         ws = self.words_left
    #         if len(ws) == 1:
    #             print(f"The word is '{ws[0]}'")
    #             return
    #         print(
    #             f'There are {len(ws)} possible words remaining {ws if len(ws) < 10 else str(ws[:10])[:-1] + ", ...]"}')

    def adjust_letters(self, guess_word, score):
        for res, letter in zip(score, guess_word.upper()):
            if res == '0':
                self.letters.black_letters += letter
            if res == '1':
                self.letters.yellow_letters += letter
            elif res == '2':
                self.letters.green_letters += letter

    def get_letters(self, word):
        result_string = ''
        for l in word:
            r = '9'
            if l in self.letters.black_letters:
                r = '0'
            if l in self.letters.yellow_letters:
                r = '1'
            if l in self.letters.green_letters:
                r = '2'
            result_string += r
        return result_string

    # def play(self):
    #     alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    #     black_letters = ''
    #     yellow_letters = ''
    #     green_letters = ''
    #
    #     def get_coloured_letter(l, colour):
    #         c = '\x1B['
    #         if colour == 'green':
    #             return f'{c}1;37;42m{l}{c}0m'
    #         if colour == 'yellow':
    #             return f'{c}1;37;43m{l}{c}0m'
    #         if colour == 'grey':
    #             return f'{c}2;30;47m{l}{c}0m'
    #         if colour == 'black':
    #             return l
    #
    #     print(
    #         '\x1B[1;32;40myou can type HELP if you get stuck, EXIT to quit, WL to see how many words are left, CTRL+L to clear the console\x1B[0m\n')
    #     result = ''
    #     count = 0
    #     all_answers = ''
    #     while result != '22222':
    #         count += 1
    #         word = self.get_valid_word()
    #         if not word:
    #             print('quitter..!')
    #             return
    #         result = self.guess(word)
    #         coloured_word = ''
    #         for res, letter in zip(result, word.upper()):
    #             if res == '0':
    #                 c_l = get_coloured_letter(letter, 'black')
    #                 black_letters += letter
    #             if res == '1':
    #                 c_l = get_coloured_letter(letter, 'yellow')
    #                 yellow_letters += letter
    #             elif res == '2':
    #                 c_l = get_coloured_letter(letter, 'green')
    #                 green_letters += letter
    #             coloured_word += c_l
    #         all_answers += '\n' + coloured_word
    #         coloured_alphabet = ''
    #         for l in alphabet:
    #             c_l = get_coloured_letter(l, 'grey')
    #             if l in black_letters:
    #                 c_l = get_coloured_letter(l, 'black')
    #             if l in yellow_letters:
    #                 c_l = get_coloured_letter(l, 'yellow')
    #             if l in green_letters:
    #                 c_l = get_coloured_letter(l, 'green')
    #             coloured_alphabet += c_l
    #         print(all_answers + '\n')
    #         print(coloured_alphabet + '\n')
    #         if result == '22222':
    #             break
    #         self.words_left = self.check(word, result)
    #
    #     print(f'Congratulations! you took {count} guesses')
    #     if self.helps > 1:
    #         print(f'...but you asked for help {self.helps} times')
    #     elif self.helps > 0:
    #         print(f'...but you asked for help')

    def get_result_word_from_pin(self):
        # TODO Make this cleverer
        if self.letters_in_word == 7:
            return self.result_words[(int(self.pin) - 50000 - date.today().toordinal()) % len(self.result_words)]
        elif self.letters_in_word == 3:
            return self.result_words[(int(self.pin) - 100 - date.today().toordinal()) % len(self.result_words)]
        else:
            return self.result_words[(int(self.pin) - 2500 - date.today().toordinal()) % len(self.result_words)]

    def get_pin_from_result_word(self, result_word):
        # TODO Make this cleverer
        result_index = self.result_words.index(result_word)
        if self.letters_in_word == 7:
            return (date.today().toordinal() + result_index) % len(self.result_words) + 50000
        elif self.letters_in_word == 3:
            return (date.today().toordinal() + result_index) % len(self.result_words) + 100
        else:
            return (date.today().toordinal() + result_index) % len(self.result_words) + 2500


    def guess(self, word: str):
        rw = self.result_word
        result, remaining_word, remaining_result = {}, {}, ''
        # first take the 2's out
        for i, letter in enumerate(word):
            if rw[i] == letter:
                result[i] = '2'
            else:
                remaining_word[i] = letter
                remaining_result += rw[i]
        for i, rl in remaining_word.items():
            if rl in remaining_result:
                result[i] = '1'
                remaining_result = remaining_result.replace(rl, '', 1)
            else:
                result[i] = '0'
        final_result = ''.join([v[1] for v in sorted(result.items())])
        self.words_left = self.check(word, final_result)
        self.adjust_letters(word, final_result)
        return final_result

    def check(self, word_guess, wordle_score):
        one_score_letters_set = {letter for letter, ws in zip(word_guess, wordle_score) if ws == '1'}
        one_score_letters_dict = {}
        for os_letter in one_score_letters_set:
            has_zeros = False
            number_of_ones = 0
            ones_index_set = set(range(self.letters_in_word))
            twos_index_set = set()
            for i, (letter, ws) in enumerate(zip(word_guess, wordle_score)):
                if letter == os_letter:
                    ones_index_set.remove(i)
                    if ws == '0':
                        has_zeros = True
                    elif ws == '1':
                        number_of_ones += 1
                    elif ws == '2':
                        twos_index_set.add(i)
            one_score_letters_dict[os_letter] = (has_zeros, number_of_ones, ones_index_set, twos_index_set)
        word_list = self.words_left.copy()
        words2 = word_list.copy()
        # check 2s
        for i, (letter, ws) in enumerate(zip(word_guess, wordle_score)):
            if letter not in one_score_letters_dict and ws == '2':
                words2 = [word2.replace(letter, '', 1) for word, word2 in zip(word_list, words2) if word[i] == letter]
                word_list = [word for word in word_list if word[i] == letter]
        # check 0s
        for i, (letter, ws) in enumerate(zip(word_guess, wordle_score)):
            if letter not in one_score_letters_dict and ws == '0':
                word_list, words2 = zip(
                    *[(word, word2) for word, word2 in zip(word_list, words2) if letter not in word2])
        # check 1s - make sure there isn't a letter that scored 1 in that 1 position
        for i, (letter, ws) in enumerate(zip(word_guess, wordle_score)):
            if ws == '1':
                word_list, words2 = zip(
                    *[(word, word2) for word, word2 in zip(word_list, words2) if word[i] != letter])

        if len(one_score_letters_dict) > 0:
            new_words = []
            for word in word_list:
                try:
                    for letter, defn in one_score_letters_dict.items():
                        for idx in defn[3]:  # 2s
                            if word[idx] != letter:
                                raise ValueError('NOPE')
                        letters_in_possible_indices = len([word[i] for i in defn[2] if word[i] == letter])
                        if defn[0]:
                            if letters_in_possible_indices != defn[1]:
                                raise ValueError('NOPE')
                        else:
                            if letters_in_possible_indices < defn[1]:
                                raise ValueError('NOPE')
                    new_words.append(word)
                except ValueError:
                    pass
            word_list = new_words
        return list(word_list)

    # def get_valid_word(self):
    #     word = ''
    #     while word not in self.allowed_words:
    #         word = input('Enter real 5 letter word >').lower()
    #         if word == 'help':
    #             print(
    #                 f'{len(self.words_left)} words left {self.words_left if len(self.words_left) < 10 else str(self.words_left[:10])[:-1] + ", ...]"}')
    #             self.helps += 1
    #         elif word == 'wl':
    #             print(f'{len(self.words_left)} words left')
    #         elif word == 'exit':
    #             return None
    #
    #     return word

    @staticmethod
    def is_valid_result(result):
        for s in result:
            if s not in '012':
                return False
        return True

    # def get_valid_help_string(self):
    #     valid = False
    #     help_words = None
    #     while not valid:
    #         print(
    #             f'Enter 2 valid strings each with 5 characters which looks like: {random.choice(self.allowed_words).upper()} {self.random_result()}')
    #         help_string = input('Enter >').lower()
    #         if help_string == 'exit':
    #             return None
    #         help_words = help_string.split(' ')
    #         if len(help_words) == 2:
    #             if len(help_words[0]) == 5 and len(help_words[1]) == 5:
    #                 if help_words[0] not in self.allowed_words:
    #                     print(f'{help_words[0].upper()} is not a valid word')
    #                 elif not self.is_valid_result(help_words[1]):
    #                     print(f'{help_words[1]} must be only 0s, 1s or 2s')
    #                 else:
    #                     valid = True
    #     return help_words[0], help_words[1]
