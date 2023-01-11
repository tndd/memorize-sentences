import json
import difflib
from random import shuffle
from datetime import datetime


def test_sentences(keys, dict_genre):
    exam_paper = {}
    for key in keys:
        jp = dict_genre[key]['jp']
        en = dict_genre[key]['en']
        while True:
            print(jp)
            hint_num = 0
            ans = input()
            if ans == '-h' or ans == '--hint':
                while True:
                    hint_num = min(hint_num + 1, len(en.split()))
                    en_head = ' '.join(en.split()[:hint_num])
                    print(en_head)
                    command = input()
                    if command == '-h' or ans == '--hint':
                        continue
                    else:
                        ans = command
                        break
            if ans == en:
                print('### OK ###')
                exam_paper[key] = {
                    'input': ans,
                    'status': True,
                    'hint_num': hint_num,
                    'diff': None
                }
                break
            else:
                print('### MISS ###')
                print(f'Correct: {en}')
                diff = ''.join(difflib.unified_diff(ans.split(), en.split()))
                print(diff)
                exam_paper[key] = {
                    'input': ans,
                    'status': False,
                    'hint_num': hint_num,
                    'diff': diff
                }
                break
    return exam_paper


def get_sentence(genre):
    with open(f'data/{genre}.json', 'r') as f:
        d = json.load(f)
    return d


def get_shuffled_keys_and_dict(genre, n=None):
    d = get_sentence(genre)
    keys = list(d.keys())
    shuffle(keys)
    if n is not None:
        keys = keys[:n]
    return keys, d


def store_exam_paper(genre, exam_paper):
    with open(f'exam_paper/{genre}/{datetime.now().isoformat()}.json', 'w') as f:
        json.dump(exam_paper, f, indent=4)


def main() -> None:
    genre = 'winston_churchill'
    keys, d = get_shuffled_keys_and_dict(genre)
    exam_paper = test_sentences(keys, d)
    store_exam_paper(genre, exam_paper)


if __name__ == '__main__':
    main()
