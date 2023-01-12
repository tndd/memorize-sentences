import difflib
import json
import os
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
    return paper


def store_test_paper(paper):
    file_name = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    dir_name = f"record/{file_name.split('T')[0]}"
    os.makedirs(dir_name, exist_ok=True)
    with open(f"{dir_name}/{file_name}.json", 'w') as f:
        json.dump(paper, f, indent=4)


def main() -> None:
    # Params
    # TODO support for optional args.
    mode = TestMode.FULL
    n = 2

    # get all data of senteneces for test
    df_sentences = get_df_sentences()
    # select mode of test
    if mode == TestMode.FULL:
        record_since = 'all'
        unknown_id_value = 0 # Unanswered sentence_id are treated as "WRONG".
    if mode == TestMode.REVIEW:
        record_since = 'latest'
        unknown_id_value = 1 # Unanswered sentence_id are treated as "CORRECT".
    # get data of records for narrow down to focus on failure sentence
    df_records = get_df_records(since=record_since)
    # get series of wrong rate by sentences
    wrong_rate_by_sentences = get_sr_wrong_rate_by_sentence(df_records, df_sentences.index, unknown_id_value)
    # randomly select in proportion to wrong rate
    ids_selected = get_random_sentence_ids(wrong_rate_by_sentences, n)
    # narrow down the test sentences to only select id
    df_sentences_for_test = df_sentences.loc[ids_selected]
    # do test
    test_paper = test_sentences(df_sentences_for_test)
    # store test results
    store_test_paper(test_paper)


if __name__ == '__main__':
    main()
