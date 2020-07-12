#!/usr/bin/env python3

import json
import random

def get_questions():
    questions_file = open('./quiz.json')
    questions_obj = json.load(questions_file)
    questions_file.close()
    return questions_obj['questions']

def print_choices(choices):
    for index, choice in enumerate(choices):
        print('{}.{}'.format(index + 1, choice), '\n')

def is_correct(ans, user_answer):
    return ans == str(user_answer)

def start_quiz():
    questions = get_questions()
    points = 0
    for index, val in enumerate(questions):
        print(val['question'], '\n') # Question
        print_choices(val['options'])
        answer = input('Your answer(in number)?\n')
        if is_correct(answer, val['answer']):
            print('✓')
            points += 1
        else:
            print('✘')
    print('You got {}/{} questions correct. Hooray'.format(points, len(questions)))
    

if __name__ == "__main__":
    canPlay = input('Press y/Y to play the Game of Thrones quiz 🦁\n')
    canPlay = str(canPlay) == 'y' or str(canPlay) == 'Y'
    start_quiz() if canPlay else exit(-1)