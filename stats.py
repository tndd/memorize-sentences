import json
import re
from glob import glob

import pandas as pd


def build_df(file_path):
    with open(file_path, 'r') as f:
        d = json.load(f)
    df = pd.DataFrame.from_dict(d, orient='index')
    group_name = re.search(r"record/.*\/(.*)\.json", file_path).group(1)
    df.insert(0, 'group', group_name)
    return df


def get_df_record(since='latest'):
    record_file_paths = glob('record/*/*.json')
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


def get_sr_mean_of_selected_by_sentence(df):
    sr_mean = df.groupby('sentence_id').mean(numeric_only=True)['status'].sort_values()
    sr_mean_selected = sr_mean.apply(lambda x: max(1 - x, 0.01))
    return sr_mean_selected


def main() -> None:
    df = get_df_record('all')
    sr = get_sr_mean_of_selected_by_sentence(df)
    


if __name__ == '__main__':
    main()
