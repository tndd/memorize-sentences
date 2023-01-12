import random
from enum import Enum, auto

from broker import get_df_records, get_df_sentences


def get_sr_wrong_rate_by_sentence(df, unknown_id_value):
    sr_mean = df.groupby('sentence_id').mean(numeric_only=True)['status']
    full_sentence_ids = get_df_sentences().index
    sr_mean_filled_un = sr_mean.reindex(full_sentence_ids, fill_value=unknown_id_value)
    sr_mean_selected = sr_mean_filled_un.apply(lambda x: max(1 - x, 0.01))
    return sr_mean_selected.sort_values(ascending=False)


class GetSentencesMode(Enum):
    FULL = auto()
    REVIEW = auto()


def get_sr_probs_of_selected_ids(mode):
    if mode == GetSentencesMode.FULL:
        record_since = 'all'
        unknown_id_value = 0 # Unanswered sentence_id are treated as "WRONG".
    if mode == GetSentencesMode.REVIEW:
        record_since = 'latest'
        unknown_id_value = 1 # Unanswered sentence_id are treated as "CORRECT".
    df = get_df_records(since=record_since)
    sr = get_sr_wrong_rate_by_sentence(df, unknown_id_value)
    return sr / sr.sum()


def get_random_sentence_ids(mode=GetSentencesMode.FULL, n=None):
    prob_selected = get_sr_probs_of_selected_ids(mode)
    n = len(prob_selected) if n is None else n
    return random.choices(prob_selected.index,weights=prob_selected, k=n)


def main() -> None:
    ids = get_random_sentence_ids(mode=GetSentencesMode.FULL)
    print(ids)
    # ids = get_random_sentence_ids(mode=GetSentencesMode.REVIEW)
    # print(ids)


if __name__ == '__main__':
    main()
