from typing import Literal

class Config:
    def __init__(self, num_target_words = 0, num_context_words = 0, window_or_max_window_length  = 0):
        self.corpus = 'childes'

        self.sample_from_context_window = False
        self.sample_from_sentences = False
        self.sample_from_context_window_with_boundaries = False

        self.num_target_words: int = num_target_words
        self.num_context_words: int = num_context_words
        self.window_or_max_window_length: list[int] | int = window_or_max_window_length

        self.plot_graph: bool = True
        self.plot_dendrogram = False
        self.print_evaluation_results = False
        self.export_comparative_table: bool = False
        self.export_contingency_table: bool = False

        self.log_level: Literal['critical', 'error', 'warning', 'info', 'debug'] = 'warning' 

    def __repr__(self):
        return str(vars(self))
