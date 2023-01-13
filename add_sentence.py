import json
from collections import defaultdict
from uuid import uuid4

import pandas as pd


def update_sentence(genre, sentences):
    try:
        with open(f'./data/{genre}.json', 'r') as f:
            d = json.load(f)
    except FileNotFoundError as e:
        print(f'>> Not found genre:"{genre}". So new data is made.')
        d = dict()
    d.update(sentences)
    with open(f'./data/{genre}.json', 'w') as f:
        json.dump(d, f, indent=4, ensure_ascii=False)


def create_sentences_dict_by_genre(new_sentences):
    d = defaultdict(dict)
    for _, row in new_sentences.iterrows():
        d[row[0]][str(uuid4())] = {
            "en": row[1],
            "jp": row[2]
        }
    return d


def main() -> None:
    file_path_new_sentences = './add_sentences.tsv'
    new_sentences = pd.read_table(file_path_new_sentences, header=None)
    d = create_sentences_dict_by_genre(new_sentences)
    for genre, sentences in d.items():
        update_sentence(genre, sentences)
        print(f'Added new data genre:{genre}')
    # clear file
    with open(file_path_new_sentences, 'w') as f:
        f.seek(0)
        f.truncate()
    print('Clear added new sentences data.')


if __name__ == '__main__':
    main()
