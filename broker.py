import json
import re
from glob import glob

import pandas as pd


def _build_df_sentence(file_path):
    with open(file_path, 'r') as f:
        d = json.load(f)
    df = pd.DataFrame.from_dict(d, orient='index')
    df.index.name = 'id'
    df.insert(0, 'group', re.search(r"\/([a-z_]+)\.json", file_path).group(1))
    return df


def get_df_sentences(shuffle=True):
    sentences_file_paths = glob('data/*.json')
    dfs = [_build_df_sentence(fp) for fp in sentences_file_paths]
    if shuffle:
        return pd.concat(dfs).sample(frac=1)
    else:
        return pd.concat(dfs)


def _build_df_record(file_path):
    with open(file_path, 'r') as f:
        d = json.load(f)
    df = pd.DataFrame.from_dict(d, orient='index')
    group_name = re.search(r"record/.*\/(.*)\.json", file_path).group(1)
    df.insert(0, 'group', group_name)
    return df


def get_df_records(since='latest'):
    record_file_paths = glob('record/*/*.json')
    df = pd.concat([_build_df_record(fp) for fp in record_file_paths])
    df.index.name = 'sentence_id'
    df = df.reset_index()
    if since == 'all':
        return df
    elif since == 'latest':
        latest_date = df['group'].max()
        return df[df['group'] == latest_date]
    else:
        return df[df['group'] >= since]
