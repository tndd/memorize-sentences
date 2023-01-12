def get_sr_wrong_rate_by_sentence(df_records, sentence_ids, unknown_id_value):
    sr_mean = df_records.groupby('sentence_id').mean(numeric_only=True)['status']
    sr_mean_filled_un = sr_mean.reindex(sentence_ids, fill_value=unknown_id_value)
    sr_mean_selected = sr_mean_filled_un.apply(lambda x: max(1 - x, 0.01))
    return sr_mean_selected.sort_values(ascending=False)


def get_random_sentence_ids(wrong_rate_by_sentences, n=None):
    prob_selected = wrong_rate_by_sentences / wrong_rate_by_sentences.sum()
    n = len(prob_selected) if n is None else n
    return prob_selected.sample(n, weights=prob_selected).index


def main() -> None:
    pass


if __name__ == '__main__':
    main()
