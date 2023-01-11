import difflib
import json
import re
from datetime import datetime
from glob import glob

import pandas as pd


def build_df(file_path):
    with open(file_path, 'r') as f:
        d = json.load(f)

    df = pd.DataFrame.from_dict(d, orient='index')
    df.index.name = 'id'
    df.insert(0, 'group', re.search(r"\/([a-z_]+)\.json", file_path).group(1))
    return df


def get_df_sentences(shuffle=True):
    sentences_file_paths = glob('data/*.json')
    dfs = [build_df(fp) for fp in sentences_file_paths]
    if shuffle:
        return pd.concat(dfs).sample(frac=1)
    else:
        return pd.concat(dfs)


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
    with open(f'exam_paper/{datetime.now().isoformat()}.json', 'w') as f:
        json.dump(paper, f, indent=4)


def main() -> None:
    df = get_df_sentences()
    test_sentences(df, n=1)


if __name__ == '__main__':
    main()
