"""Placeholder for the V1 model (BoostMetric), which is not part of this repository.

aad_metric.py and aad_metric_gmm.py import BoostMetric at module level, but only the deprecated
V1 path uses it; the paper's setting (--v2) never does. This placeholder lets the import succeed
and fails loudly if anything tries to use V1.
"""


class BoostMetric:
    def __init__(self, *args, **kwargs):
        raise RuntimeError("BoostMetric (V1) is not included in this repository; run with --v2")
