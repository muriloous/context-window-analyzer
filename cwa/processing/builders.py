from .contingency_table import ContingencyTable
from preprocessing import (
  get_most_common_words,
  is_boundary_marker
)

def build_contingency_dicts_from_context_window(
        tokens: list[str],
        num_target_words: int = 300,
        num_context_words: int = 100,
        window: list[int] = [-2, -1, 1, 2],
        with_boundaries = False
        ) -> ContingencyTable:
    '''
    Build contingency dicts from the specified context window
    '''
    if isinstance(window, int): window = [*range(- window, 0), *range(1, window + 1)]

    common_words = get_most_common_words(tokens, max(num_context_words, num_target_words), (not with_boundaries))
    target_words = common_words[:num_target_words]
    context_words = common_words[:num_context_words]

    contingency_table = ContingencyTable(target_words, context_words, window)

    tokens_list_length = len(tokens)
    for idx, token in enumerate(tokens):
        if not token in target_words: continue

        for position_idx, position in enumerate(window):
            relative_token_idx = idx + position
            if relative_token_idx < 0 or relative_token_idx >= tokens_list_length: continue
            relative_token = tokens[relative_token_idx]
            context_idx = next((idx for idx, word in enumerate(context_words) if word == relative_token), None)
            if context_idx == None: continue
            contingency_vector_idx = num_context_words * position_idx + context_idx
            contingency_table.data[token][contingency_vector_idx] += 1

    return contingency_table
    
def build_contingency_dicts_from_sentences(
        tokens: list[str],
        num_target_words: int = 300,
        num_context_words: int = 100,
        max_window_length: int = 2
        ) -> ContingencyTable:
    '''
    Build contingency dicts directly from sentence boundaries
    '''
    if isinstance(max_window_length, list): max_window_length = abs(max(max_window_length, key=abs))
    window = [*range(- max_window_length, 0), *range(1, max_window_length + 1)]
    
    common_words = get_most_common_words(tokens, max(num_context_words, num_target_words), remove_boundary_markers=True)
    target_words = common_words[:num_target_words]
    context_words = common_words[:num_context_words]

    contingency_table = ContingencyTable(target_words, context_words, window)
    
    tokens_list_length = len(tokens)
    for idx, token in enumerate(tokens):
        if not token in target_words: continue

        for inc in [-1, 1]:
            rel_idx = idx + inc
            idx_distance = 1
            while   rel_idx > -1 and \
                    rel_idx < tokens_list_length and \
                    idx_distance <= max_window_length:
                relative_token = tokens[rel_idx]
                rel_idx += inc
                idx_distance += 1

                if is_boundary_marker(relative_token): break
                if not relative_token.isalnum(): continue

                context_idx = next((idx for idx, word in enumerate(context_words) if word == relative_token), None)
                if context_idx == None: continue

                # position_idx = inc * (idx_distance - 1) + max_window_length + (-1 if inc == 1 else 0)
                position_idx = next((idx for idx, position in enumerate(window) if position == inc * (idx_distance - 1)))
                contingency_vector_idx = (num_context_words * position_idx) + context_idx

                contingency_table.data[token][contingency_vector_idx] += 1

    return contingency_table
