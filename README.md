# README

## Updates in this fork

This is a copy of the [original PMA repository](https://github.com/taylordinkins/PrecisionMatrixAdjustments) with the changes below. Everything else is unchanged, and the original commands below still reproduce the paper's numbers.

1. **Optimizer fix (always on).** `optimize_w_fast` (the anomaly update, in `aad_metric_model_v2.py` and `aad_metric_model_gmm.py`) now computes the deviation with the precision matrix A, as in Eq. 1, instead of its inverse, and uses the correct trace of diag(w) Z diag(w) in the penalty. On the datasets we reran, this gives the same results as the paper: queried anomalies are far past the threshold, so the loss gradient is near zero either way.
2. **Sherman–Morrison nominal update (opt-in).** `--sm_nominal` replaces the nominal update, which subtracts at most the smallest eigenvalue and so barely moves scores after the first nominal label, with A ← A − η A u uᵀ A / (1 + η uᵀ A u). Here η brings the labeled point's score toward the median score under the starting matrix, damped by `--sm_alpha` (default 0.5). A stays positive definite without a cap.

```
python src/aad_metric.py --data_path "$data_path" --data msl --iters 50 --k 3 --v 1e-7 --original_mu --nom_deweight --conserv_thresh 50 --true_feedback --full_k --v2 --sm_nominal --save_suffix v2_nominal_sm
```

The flag works the same way for `aad_metric_gmm.py` (PMA-MGE).

3. **Faster scoring and anomaly updates (always on).** Anomaly scores are computed with one batched matrix product instead of a per-point loop, and the anomaly update no longer computes an SVD and a matrix inverse whose results it never uses. Results are identical to the version without this change; the update loop runs about 2–3× faster on 512-dimensional data, so runtimes from this version differ from those reported in the paper.

`src/aad_metric_model.py` is a placeholder for the unused V1 model so the scripts import, and the empty `figures/`, `results_runtimes/`, `results_kmeans_reduced/` and `results_gmms_seeds/` folders are folders the scripts write to.

---

This repository contains the code for the paper **"Incorporating Interactive User Feedback through Precision Matrix Adjustments for High-Dimensional Anomaly Detection"**, published and presented at ICDM 2025.

## To Collect the Results from the Paper

1. Run example experiments:
    First, change the ```data_path``` variable in ```run_pma.sh``` to the path containing the processed data - typically this is ```./data/``` To collect all numbers from the paper results section for PMA and PMA-MGE, as well as the default Mahalanobis distance MD, simply run
    ```
    bash src/run_pma.sh
    ```

    These are automatically saved to the respective results folders.

2. Competitor experiments:
    GAOD uses the same code-base here. To collect these numbers, run 
    ```
    bash src/run_gaod.sh
    ```

    AAD-IF and AAD-LODA are found in [this repository](https://github.com/shubhomoydas/ad_examples/tree/master). F1 and AUPRC were calculated from anomaly scores and saved each iteration after the budget is exhausted. 

    FIF is found in [this repository](https://github.com/siddiqmd/FeedbackIsolationForest). Similarly, F1 and AUPRC were calculated each iteration using the anomaly scores. 

    SOEL is found in [this repository](https://github.com/aodongli/Active-SOEL/tree/main/NTL). Once again, the anomaly scores are used for F1 and AUPRC. This base was used for image embeddings

    Runtime calculations were done for the iterative portions of the algorithms, and any optimization or model updates. 

    Please see the paper for experimental setups in all cases (hyperparameters, model specifications, etc.). 

    Plots of runtime vs AUPRC/FI are constructed using ```python src/plotting.py```, and SOEL results are processed using ```python src/dl_comparison.py```. Statistical significance testing is done with ```python src/wilcoxon_tests.py```. Latex table creation is done with ```python src/process_fif.py```. In all cases, there are variables for the base directories at the start of each function that should be set. These should contain the respective results txt or csv files. Naming conventions on most files are fixed currently with the anomaly score processing for each algorithm. If collecting results from AAD-IF/LODA, FIF, or SOEL, these should be consistent, or modified accordingly. We include the collected and saved runtimes and F1/AUPRC scores from these four algorithms in their various results folders here for easy access, which were used for the paper. 

3. MSL and MNIST/KMNIST Pretrained Models:
    The pretrained models for the Mars Science Laboratory (MSL) and MNIST are found in ```./models/```. These were used to extract feature embeddings for these two datasets. 

4. Data:
    The processed data can be found at [this link](https://drive.google.com/file/d/1_aM7PEILJL1iriV8bHrO9A40cHhrDLRn/view?usp=drive_link). Vision datasets were processed using ```torch_processing.py```, outside of the SOEL experiments, which were saved from the SOEL repository code. 




