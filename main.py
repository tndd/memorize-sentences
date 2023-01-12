import difflib
import json
import os
import random
from datetime import datetime
from enum import Enum, auto

from broker import get_df_records, get_df_sentences
from stats import get_random_sentence_ids, get_sr_wrong_rate_by_sentence


class TestMode(Enum):
    FULL = auto()
    REVIEW = auto()


def test_sentences(sentences, n=None):
    paper = {}
    n = len(sentences) if n is None else n
    for index, row in sentences[:n].iterrows():
        while True:
            print(row['jp'])
            hint_num = 0
            ans = input()
            if ans == '-h' or ans == '--hint':
                while True:
                    hint_num = min(hint_num + 1, len(row['en'].split()))
                    en_head = ' '.join(row['en'].split()[:hint_num])
                    print(en_head)
                    command = input()
                    if command == '-h' or ans == '--hint':
                        continue
                    else:
                        ans = command
                        break
            if ans == row['en']:
                print('### OK ###')
                paper[index] = {
                    'input': ans,
                    'status': True,
                    'hint_num': hint_num,
                    'diff': None
                }
                break
            else:
                print('### MISS ###')
                print(f"Correct: {row['en']}")
                diff = ''.join(difflib.unified_diff(ans.split(), row['en'].split()))
                print(diff)
                paper[index] = {
                    'input': ans,
                    'status': False,
                    'hint_num': hint_num,
                    'diff': diff
                }
                break
    file_name = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    dir_name = f"record/{file_name.split('T')[0]}"
    os.makedirs(dir_name, exist_ok=True)
    with open(f"{dir_name}/{file_name}.json", 'w') as f:
        json.dump(paper, f, indent=4)


def main() -> None:
    # Params
    mode = TestMode.FULL
    n = 2

    df_sentences = get_df_sentences()
    if mode == TestMode.FULL:
        record_since = 'all'
        unknown_id_value = 0 # Unanswered sentence_id are treated as "WRONG".
    if mode == TestMode.REVIEW:
        record_since = 'latest'
        unknown_id_value = 1 # Unanswered sentence_id are treated as "CORRECT".
    df_records = get_df_records(since=record_since)
    wrong_rate_by_sentences = get_sr_wrong_rate_by_sentence(df_records, df_sentences.index, unknown_id_value)
    ids_choiced = get_random_sentence_ids(wrong_rate_by_sentences, n)
    df_sentences_for_test = df_sentences.loc[ids_choiced]
    test_sentences(df_sentences_for_test)


if __name__ == '__main__':
    main()
