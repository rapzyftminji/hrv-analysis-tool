# ASN Analysis Tools

This folder contains tools for analyzing physiological data extracted from PPG signals and correlating them with DASS-21 scores.

## Files

- `analysistools.py`: The main analysis script. It performs statistical analysis, correlation checks, and generates visualizations.
- `converter.py`: A utility script to convert the raw Excel file (`Ekstraksi Fitur.xlsx`) into the CSV format required by the analysis tool.
- `Ekstraksi_Fitur_Converted.csv`: The input data file for `analysistools.py`.

## Prerequisites

Make sure you have the required Python libraries installed:

```bash
pip install pandas matplotlib seaborn numpy openpyxl
```

## Usage

### 1. Data Conversion (Optional)
If you have your data in an Excel file named `Ekstraksi Fitur.xlsx`, run the converter to generate the CSV:

```bash
python3 converter.py
```
*Note: Check `converter.py` to ensure `HEADER_ROW` matches your Excel file structure.*

### 2. Run Analysis
Run the main analysis script:

```bash
python3 analysistools.py
```

## Outputs

The script will create two folders with the results:

### `Analysis Result/` (Visualizations)
- **Correlation Matrix Heatmap**: `correlation_matrix_heatmap.png`
- **Scatter Plots**: `analysis_plots_part_X.png` (Scatter plots of each metric vs DASS-21 score with regression lines)
- **Box Plots**: `box_plots_part_X.png` (Distribution of metrics grouped by severity)

### `Statistic/` (Data Tables)
- **Correlation Results**: `correlation_results.csv` (Correlation coefficients for all metrics)
- **Grouped Statistics**: `grouped_statistics.csv` (Mean and Standard Deviation for each metric grouped by Severity)
- **Sorted Data**: `sorted_analyzed_data.csv` (The processed dataset sorted by DASS-21 score)

## Metrics Analyzed
The tools analyze 24 physiological metrics including:
- Heart Rate (HR)
- Respiratory Rate
- HRV Metrics (SDNN, RMSSD, pNN50, etc.)
- Frequency Domain Metrics (LF, HF, LF/HF Ratio)
- Non-linear Metrics (SD1, SD2)

## Severity Categories
DASS-21 scores are categorized as:
- **Normal**: 0-7
- **Ringan**: 8-9
- **Sedang**: 10-12
- **Parah**: 13-16
- **Sangat Parah**: >16
