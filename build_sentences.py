import json
import pandas as pd


def build_df(group):
    with open(f'data/{group}.json', 'r') as f:
        d = json.load(f)

    df = pd.DataFrame.from_dict(d, orient='index')
    df.index.name = 'id'
    df.insert(0, 'group', group)
    return df


def main() -> None:
    df = build_df('winston_churchill')
    df.to_csv('data/sentences.tsv', sep='\t')


if __name__ == '__main__':
    main()
