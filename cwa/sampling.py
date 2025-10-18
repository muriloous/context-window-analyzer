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
    match (sample_from):
        case 'context_window':
            return sample_from_context_window(corpus, num_target_words, num_context_words, window_or_max_window_length)
        case 'context_window_with_boundaries':
            return sample_from_context_window_with_boundaries(corpus, num_target_words, num_context_words, window_or_max_window_length)
        case 'sentences':
            return sample_from_sentences(corpus, num_target_words, num_context_words, window_or_max_window_length)
        case _:
            raise Exception(f'"{sample_from}" is not a valid sampling option')

def sample_from_sentences(
        corpus: str | list[str],
        num_target_words: int,
        num_context_words: int,
        max_window_length: int | list[int]
    ):

  tokens = prepare_corpus(corpus)

  lowered_tokens = get_lower_tokens(tokens)

  return build_contingency_dicts_from_sentences(lowered_tokens, num_target_words, num_context_words, max_window_length)

def sample_from_context_window(
      corpus: str | list[str],
      num_target_words: int,
      num_context_words: int,
      window: list[int] | int
    ):

  tokens = prepare_corpus(corpus)

  lowered_tokens = get_lower_words(tokens)

  return build_contingency_dicts_from_context_window(lowered_tokens, num_target_words, num_context_words, window)

def sample_from_context_window_with_boundaries(
      corpus: str | list[str],
      num_target_words: int,
      num_context_words: int,
      window: list[int] | int
    ):

  tokens = prepare_corpus(corpus)

  lowered_tokens = get_lower_tokens(tokens)

  return build_contingency_dicts_from_context_window(lowered_tokens, num_target_words, num_context_words, window)