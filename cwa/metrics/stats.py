import itertools, random, logging
from numpy._typing import NDArray
import numpy as np
import scipy.cluster.hierarchy as hac
from scipy.stats import spearmanr
from scipy.spatial.distance import squareform

from processing import ContingencyTable
from .evaluation_result import EvaluationResult

def vectorize_contingency_table(contingency_table: ContingencyTable) -> NDArray:
    return np.array(list(contingency_table.data.values()))

def get_linkage_matrix(matrix: NDArray) -> NDArray:
    logging.debug('\nMatrix\n' + repr(matrix))

    coef, _ = spearmanr(matrix, axis=1)
    logging.debug('\nSpearman coef\n' + repr(coef))

    normalized_matrix = (coef + 1) / 2
    logging.debug('\nNormalized matrix\n' + repr(normalized_matrix))

    distance_matrix = 1 - normalized_matrix
    distance_matrix = np.nan_to_num(distance_matrix, nan=1.0, posinf=1.0, neginf=1.0)
    logging.debug('\nDistance matrix\n' + repr(distance_matrix))

    condensed_distance = squareform(distance_matrix, checks=False)
    logging.debug('\nCondensed matrix (distance squareform)\n' + repr(condensed_distance))
    
    linkage_matrix = hac.linkage(condensed_distance, method='average')
    logging.debug('\nLinkage matrix\n' + repr(linkage_matrix))

    return linkage_matrix

def evaluate(contingency_table: ContingencyTable , tagged_data) -> EvaluationResult:  
  matrix = vectorize_contingency_table(contingency_table)

  linkage_matrix = get_linkage_matrix(matrix)

  tags_per_word = {}
  for word, tag in tagged_data:
    key = word.lower()
    if not key in tags_per_word: tags_per_word[key] = []
    if not tag in tags_per_word[key]: tags_per_word[key].append(tag)
  
  return evaluate_clusters(linkage_matrix, contingency_table.target_words, tags_per_word)

def evaluate_clusters(
      linkage_matrix: NDArray,
      target_words: list[str],
      corpus_ref: dict[str, list[str]],
      beta: int = 0.3,
      n_baseline: int = 10
    ) -> dict[str, float | int | dict[str, int]]:

    best = EvaluationResult()

    ref_pairs = set(
        (a, b) for a, b in itertools.combinations(target_words, 2)
        if a in corpus_ref and b in corpus_ref and set(corpus_ref[a]) & set(corpus_ref[b])
    )

    for cut in np.arange(0.0, 1.0, 0.01):
        labels = hac.fcluster(linkage_matrix, cut, criterion='distance')
        cluster_map = {word: labels[i] for i, word in enumerate(target_words)}

        test_pairs = set(
            (a, b) for a, b in itertools.combinations(target_words, 2)
            if cluster_map[a] == cluster_map[b]
        )

        tp = len(test_pairs & ref_pairs)
        fp = len(test_pairs - ref_pairs)
        fn = len(ref_pairs - test_pairs)

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        comp = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        f = ((1 + beta**2) * prec * comp) / (beta**2 * prec + comp) if (beta**2 * prec + comp) > 0 else 0.0

        baseline_fs = []
        for _ in range(n_baseline):
            shuffled = list(cluster_map.values())
            random.shuffle(shuffled)
            random_map = {word: shuffled[i] for i, word in enumerate(target_words)}

            random_pairs = set(
                (a, b) for a, b in itertools.combinations(target_words, 2)
                if random_map[a] == random_map[b]
            )

            tp_b = len(random_pairs & ref_pairs)
            fp_b = len(random_pairs - ref_pairs)
            fn_b = len(ref_pairs - random_pairs)

            prec_b = tp_b / (tp_b + fp_b) if (tp_b + fp_b) > 0 else 0.0
            comp_b = tp_b / (tp_b + fn_b) if (tp_b + fn_b) > 0 else 0.0
            f_b = ((1 + beta**2) * prec_b * comp_b) / (beta**2 * prec_b + comp_b) if (prec_b + comp_b) > 0 else 0.0

            baseline_fs.append(f_b)

        avg_baseline = np.mean(baseline_fs)

        result = EvaluationResult(
            cut=cut,
            f_score=f,
            baseline_f=avg_baseline,
            precision=prec,
            completeness=comp,
            n_clusters=len(set(labels))
        )
        
        best.curve.append(result)

        if f > best.f_score:
            best.update_metrics(result)
            best.labels = cluster_map
            
    return best
