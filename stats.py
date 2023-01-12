import random
from enum import Enum, auto

from broker import get_df_records, get_df_sentences


def get_sr_mean_of_selected_by_sentence(df, unknown_id_value):
    sr_mean = df.groupby('sentence_id').mean(numeric_only=True)['status']
    idxs = get_df_sentences().index
    # Unanswered sentence_id shall be assumed to have been answered wrong.
    sr_mean = sr_mean.reindex(idxs, fill_value=unknown_id_value)
    sr_mean_selected = sr_mean.apply(lambda x: max(1 - x, 0.01))
    return sr_mean_selected.sort_values(ascending=False)


class GetSentencesMode(Enum):
    FULL = auto()
    REVIEW = auto()


def get_random_sentence_ids(mode=GetSentencesMode.FULL, n=None):
    if mode == GetSentencesMode.FULL:
        record_since = 'all'
        unknown_id_value = 0 # Unanswered sentence_id are treated as "WRONG".
    if mode == GetSentencesMode.REVIEW:
        record_since = 'latest'
        unknown_id_value = 1 # Unanswered sentence_id are treated as "CORRECT".
    df = get_df_records(since=record_since)
    sr = get_sr_mean_of_selected_by_sentence(df, unknown_id_value)
    prob = sr / sr.sum()
    print(prob)
    n = len(sr) if n is None else n
    return random.choices(sr.index,weights=prob, k=n)


def main() -> None:
    ids = get_random_sentence_ids(mode=GetSentencesMode.FULL)
    print(ids)
    ids = get_random_sentence_ids(mode=GetSentencesMode.REVIEW)
    print(ids)


if __name__ == '__main__':
    main()
