from typing import Literal

from preprocessing import (
   prepare_corpus,
   get_lower_tokens,
   get_lower_words
)

from processing import (
   build_contingency_dicts_from_context_window,
   build_contingency_dicts_from_sentences
)

sample_from_type = Literal['context_window', 'sentences', 'context_window_with_boundaries']

def sample_from(
        corpus: str | list[str],
        sample_from: sample_from_type,
        num_target_words: int,
        num_context_words: int,
        window_or_max_window_length: int
    ):
    tokens = prepare_corpus(corpus)

    lowered_tokens = get_lower_tokens(tokens)

    match (sample_from):
        case 'context_window':
            return build_contingency_dicts_from_context_window(lowered_tokens, num_target_words, num_context_words, window_or_max_window_length, with_boundaries = False)
        case 'context_window_with_boundaries':
            return build_contingency_dicts_from_context_window(lowered_tokens, num_target_words, num_context_words, window_or_max_window_length, with_boundaries = True)
        case 'sentences':
            return build_contingency_dicts_from_sentences(lowered_tokens, num_target_words, num_context_words, window_or_max_window_length)
        case _:
            raise Exception(f'"{sample_from}" is not a valid sampling option')
