OPTIONS = {
    'help': {
        'tag': {'h', 'help'},
        'require_arguments': False,
        'description': "Display this help and exit"
    },

    'verbose': {
        'tag': {'v', 'verbose',},
        'require_arguments': False,
        'description': 'Sets log level to verbose.'
    },

    'debug': {
        'tag': {'debug'},
        'require_arguments': False,
        'description': 'Sets log level to debug.'
    },

    'corpus': {
      'tag': {'corpus', 'corpora'},
      'require_arguments': True,
      'description': 'Set the corpora to use',
      'example': '--corpora=childes'
    },

    'sample_from': {
        'tag': {'s', 'sample-from'},
        'require_arguments': True,
        'description': 'Option used to select data processing method: can be either "context-window"/"ctx" or "sentences"/"sent"',
        'example': '--sample-from=context-window,sentences | --sample-from=context-window-with-boundaries | -s ctx,ctx-bound | -s sent',
        'arguments': {
            'context_window': {'context-window', 'ctx-window', 'ctx', 'ctx-no-bound'},
            'context_window_with_boundaries': {'context-window-with-boundaries', 'ctx-window-bound', 'ctx-bound'},
            'sentences': {'sentences', 'sentence', 'sent'},
        },
    },

    'num_context_words': {
        'tag': {'c', 'context-words', 'num-context-words'},
        'require_arguments': True,
        'description': 'Number of context words to process.',
        'example': '--context-words=<int> | -c<int>',
    },

    'num_target_words': {
        'tag': {'t', 'target-words', 'num-target-words'},
        'require_arguments': True,
        'description': 'Number of target words to process.',
        'example': '--target-words=<int> | -t<int>',
    },

    'window_or_max_window_length': {
        'tag': {'w', 'window', 'context-window', 'max-window-length'},
        'require_arguments': True,
        'description': 'Number of maximum context window length or a detailed list of the desired window range. List should be written without any spaces between. If list is given, "sentences" method takes the maximum absolute value from it. If some integer i is given, "context-window" method make a list from -i to i, without 0 (zero).',
        'example': '--window=<int> | -w<int> | --window=<list[int]> | -w <list[int]>',
    },

    'plot_graph': {
        'tag': {'g', 'plot', 'plot-graph', 'graph'},
        'require_arguments': False,
        'description': '(Active by default) Plots evaluation cuts in a graph. Used in comparison functions.'
    },

    'no_plot_graph': {
        'tag': {'no-plot', 'no-plot-graph', 'no-graph'},
        'require_arguments': False,
        'description': '(Active by default) Plots evaluation cuts in a graph. Used in comparison functions.'
    },

    'plot_dendrogram': {
        'tag': {'d', 'dendrogram'},
        'require_arguments': False,
        'description': 'Shows a dendrogram built from processed data.'
    },

    'export_contingency_table': {
        'tag': {'e', 'export-contingency-table', 'contingency-table', 'contingency-dict', 'to-csv'},
        'require_arguments': False,
        'description': 'Exports a contingency table built from processed data.'
    },

    'export_comparative_table': {
        'tag': {'x', 'comparative-table', 'export-comparative-table'},
        'require_arguments': False,
        'description': 'Exports evaluation cuts to a CSV file. Used in comparison functions.'
    },

    'print_evaluation_results': {
        'tag': {'r', 'results', 'evaluation-results', 'print-evaluation-results'},
        'require_arguments': False,
        'description': 'Returns evaluation information about processed data.'
    },
}
