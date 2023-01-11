import json
import re
from glob import glob

import pandas as pd


def build_df(file_path):
    with open(file_path, 'r') as f:
        d = json.load(f)
    df = pd.DataFrame.from_dict(d, orient='index')
    df.insert(0, 'group', re.search(r"record/(.*).json", file_path).group(1))
    return df


def get_df_record(since='latest'):
    record_file_paths = glob('record/*.json')
    df = pd.concat([build_df(fp) for fp in record_file_paths])
    df.index.name = 'sentence_id'
    df = df.reset_index()
    if since == 'all':
        return df
    elif since == 'latest':
        latest_date = df['group'].max()
        return df[df['group'] == latest_date]
    else:
        return df[df['group'] >= since]


def main() -> None:
    df = get_df_record()
    print(df)
    # df_by_sentences = df.groupby('sentence_id').mean().sort_values('status')
    # print(df_by_sentences)


if __name__ == '__main__':
    main()
