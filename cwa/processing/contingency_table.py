class ContingencyTable:
    def __init__(self, target_words: list[str], context_words: list[str], window: list[int]):
        num_context_words = len(context_words)
        window_length = len(window)

        total_context_words_positions = context_words * window_length
        position_for_context_word = [position for position in window for _ in range(num_context_words)]

        self. window = window
        self.target_words = target_words
        self.context_words = context_words
        self.header: list[tuple[str, int]] = list(zip(total_context_words_positions, position_for_context_word))
        self.data: dict[str, list[int]] = {key: [0 for _ in range(window_length * num_context_words)] for key in target_words}

    def __str__(self):
        return str(vars(self))
    
    def __repr__(self):
        return str(vars(self))