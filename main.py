import difflib
from datetime import datetime
from enum import Enum, auto

import pandas as pd

from broker import (ModeGetRecord, get_df_records, get_df_sentences,
                    store_test_paper, store_test_stats)
from stats import get_random_sentence_ids, get_sr_wrong_rate_by_sentence


class TestMode(Enum):
    FULL = auto()
    RECENT = auto()
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


def get_wrong_rate_by_sentences(mode, df_sentences):
    # select mode of test
    if mode == TestMode.FULL:
        mode_record = ModeGetRecord.ALL
        unknown_id_value = 0 # Unanswered sentence_id are treated as "WRONG".
    elif mode == TestMode.RECENT:
        mode_record = ModeGetRecord.RECENT
        unknown_id_value = 0 # Unanswered sentence_id are treated as "WRONG".
    elif mode == TestMode.REVIEW:
        mode_record = ModeGetRecord.LATEST
        unknown_id_value = 1 # Unanswered sentence_id are treated as "CORRECT".
    else:
        raise
    # get data of records for narrow down to focus on failure sentence
    df_records = get_df_records(mode=mode_record)
    # get series of wrong rate by sentences
    return get_sr_wrong_rate_by_sentence(df_records, df_sentences.index, unknown_id_value)


def get_df_test_stats(df_sentences):
    mode = TestMode.FULL
    wrong_rate_by_sentences = get_wrong_rate_by_sentences(mode, df_sentences)
    return pd.merge(wrong_rate_by_sentences, df_sentences, left_index=True, right_index=True)


def main() -> None:
    # Params
    # TODO support for optional args.
    mode = TestMode.FULL
    n = 10

    # get all data of senteneces for test
    df_sentences = get_df_sentences()
    # get series of wrong rate by sentence id
    wrong_rate_by_sentences = get_wrong_rate_by_sentences(mode, df_sentences)
    # randomly select in proportion to wrong rate
    ids_selected = get_random_sentence_ids(wrong_rate_by_sentences, n)
    # narrow down the test sentences to only select id
    df_sentences_for_test = df_sentences.loc[ids_selected]
    # do test
    test_paper = test_sentences(df_sentences_for_test)
    # # store test results
    file_name = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    store_test_paper(file_name, test_paper)
    # store test stat
    df_test_stat_updated = get_df_test_stats(df_sentences)
    store_test_stats(file_name, df_test_stat_updated)



if __name__ == '__main__':
    main()
