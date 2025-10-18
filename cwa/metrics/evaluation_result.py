from typing import Literal, Callable, Any
from functools import wraps

EvaluationResultMetrics = Literal['f_score', 'cut', 'precision', 'completeness', 'baseline_f', 'n_clusters']

def refresh_metrics(method: Callable):
    @wraps(method)
    def wrapper(self: "EvaluationResult", *args, **kwargs):
        self._metrics = {
            'cut': self.cut,
            'precision': self.precision,
            'completeness': self.completeness,
            'f_score': self.f_score,
            'baseline_f': self.baseline_f,
            'n_clusters': self.n_clusters,
        }
        return method(self, *args, **kwargs)
    return wrapper

class EvaluationResult:    
    def __init__(self,
        cut: float = 0.0,
        precision: float = 0.0,
        completeness: float = 0.0,
        f_score: float = 0.0,
        baseline_f: float = 0.0,
        n_clusters: int = 0
    ) -> None:
        self.cut: float = cut
        self.precision: float = precision
        self.completeness: float = completeness
        self.f_score: float = f_score
        self.baseline_f: float = baseline_f
        self.n_clusters: int = n_clusters

        self.labels: dict[str, int] = {}
        self.curve: list[EvaluationResult] = []

        self._metrics: dict[EvaluationResultMetrics, Any] = {}
    
    @refresh_metrics
    def __repr__(self):
        return repr(self._metrics)

    @refresh_metrics
    def get(self, metric: EvaluationResultMetrics, round_by:None|int=None):
        treated = lambda prop : round(prop, round_by) if isinstance(round_by, int) else prop

        try: return treated(self._metrics[metric])
        except KeyError: raise Exception(f'No such metric as "{metric}"')
        
    def update_metrics(self, other: "EvaluationResult"):
        self.f_score = other.f_score
        self.cut = other.cut
        self.precision = other.precision
        self.completeness = other.completeness
        self.baseline_f = other.baseline_f
        self.n_clusters = other.n_clusters
