from config import Config

def run_model(config: Config):
    import logging
    from exporters import ComparativeTable
    from preprocessing import load_corpus
    from sampling import (
        sample_from,
        sample_from_type
    )

    graph_colors = None if not config.plot_graph else {
        'context_window': 'b',
        'context_window_with_boundaries': 'y',
        'sentences': 'g'
    }

    logging.info('Comparing precision, completeness and informativeness by similarity\n')

    samples: list[sample_from_type] = []
    if config.sample_from_context_window: samples.append('context_window')
    if config.sample_from_context_window_with_boundaries: samples.append('context_window_with_boundaries')
    if config.sample_from_sentences: samples.append('sentences')
    if not samples: raise Exception("No sample was selected. Use the -h option to get help.")

    metrics = ['precision', 'completeness', 'f_score']
    comparative_table = None if not config.export_comparative_table else ComparativeTable(metrics, samples)
    tokens, tagged_data = load_corpus(config.corpus)
    logging.info('\nProcessed tokens:' + repr(len(tokens)) + '\n')

    graph_plots = []
    for sample in samples:
        logging.info(f'Sampling from {sample}...')

        contingency_table = sample_from(
            tokens,
            sample,
            config.num_target_words,
            config.num_context_words,
            config.window_or_max_window_length
        )
        if config.plot_dendrogram:
            from exporters import make_dendrogram
            logging.info(f'Plotting dendrogram for sample from {sample}...')
            make_dendrogram(contingency_table)
        if config.export_contingency_table:
            from exporters import export_contingency_table_to_csv
            logging.info(f'Exporting contingency table for sample from {sample}...')
            export_contingency_table_to_csv(contingency_table, sample)

        if not (
            config.print_evaluation_results or
            config.export_comparative_table or
            config.plot_graph
        ): 
            logging.info('')
            continue
        
        logging.info(f'Evaluating results for sample from {sample}...')
        from metrics import evaluate
        result = evaluate(contingency_table, tagged_data)
        if config.print_evaluation_results: print(result)
        if config.export_comparative_table:
            for metric in metrics: comparative_table.add(metric, sample, result.get(metric, 2))

        if config.plot_graph:
            logging.info(f'Plotting graph for sample from {sample}...')
            x = [p.cut for p in result.curve]
            precision = [p.precision for p in result.curve]
            completeness = [p.completeness for p in result.curve]
            f_score = [p.f_score for p in result.curve]
            baseline = [p.baseline_f for p in result.curve]

            graph_plots.append((x, precision, f'{graph_colors[sample]}-', f'Precision [{sample}]', 1))
            graph_plots.append((x, completeness, f'{graph_colors[sample]}:', f'Completeness [{sample}]', 1))
            graph_plots.append((x, f_score, f'{graph_colors[sample]}--', f'F-score [{sample}]', 1))
            graph_plots.append((x, baseline, f'{graph_colors[sample]}--', f'Baseline [{sample}]', 0.3))
        
        logging.info('')


    if config.export_comparative_table:
        from exporters import export_comparative_table
        export_comparative_table(comparative_table)
    
    if config.plot_graph:
        import matplotlib.pyplot as plt
        plt.figure() 
        for x, y, style, label, alpha in graph_plots:
            plt.plot(x, y, style, label=label, alpha=alpha)
        plt.xlabel('Similarity level (cut)')
        plt.ylabel('Precision/Completeness/F-score')
        plt.title('Performance by similarity level comparison')
        plt.legend()
        plt.grid(True)
        plt.show()