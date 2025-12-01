import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
import os

# --- Configuration ---
FILE_NAME = 'Ekstraksi_Fitur_Converted.csv' 
RESULT_DIR = 'Analysis Result'
STAT_DIR = 'statistic'

# Create directories if they don't exist
os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(STAT_DIR, exist_ok=True)

# These are the headers you provided, in order
HEADERS = [
    "HR", "Resp Rate (BrPm)", "Vasometric freq (Hz)", "SDNN Index (ms)", "RMSSD (ms)",
    "SDSD", "NN50", "pNN50 (%)", "HTI", "TINN (ms)", "CVNN", "CVSD",
    "Skewness of NN Distribution", "TP (ms2)", "TP of LF (ms2)", "TP of HF (ms2)",
    "LF/HF Ratio", "LF (n.u.)", "HF (n.u)", "Peak Frequency of LF (Hz)",
    "Peak Frequency of HF (Hz)", "SD1", "SD2", "SD1/SD2", "DASS-21"
]

def analyze_raw_data(filepath):
    print(f"Loading data from {filepath}...")
    
    # 1. Load Data
    try:
        # Load data without header, using the provided HEADERS list
        df = pd.read_csv(filepath, header=None, names=HEADERS)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return

    # 2. Sort by DASS-21 (Low -> High)
    print("Sorting data by DASS-21...")
    df.sort_values(by='DASS-21', ascending=True, inplace=True)
    
    # 3. Create Severity Category
    def categorize_severity(score):
        if score <= 7: return 'Normal'
        elif score <= 9: return 'Ringan'
        elif score <= 12: return 'Sedang'
        elif score <= 16: return 'Parah'
        else: return 'Sangat Parah'

    df['Severity'] = df['DASS-21'].apply(categorize_severity)
    severity_order = ['Normal', 'Ringan', 'Sedang', 'Parah', 'Sangat Parah']

    # 4. Correlation Analysis
    print("\n--- Calculating Correlations ---")
    # Select only numeric columns for correlation
    numeric_df = df.select_dtypes(include=[np.number])
    
    if 'DASS-21' in numeric_df.columns:
        correlations = numeric_df.corr()['DASS-21'].sort_values(ascending=False)
        
        print("Top 5 Positive Correlations:")
        print(correlations.head(6)[1:]) # Skip DASS-21 itself
        print("\nTop 5 Negative Correlations:")
        print(correlations.tail(5))
        
        correlations.to_csv(os.path.join(STAT_DIR, 'correlation_results.csv'))
        print(f"Full correlation results saved to '{STAT_DIR}/correlation_results.csv'")

        # --- Correlation Matrix Heatmap ---
        print("Generating Correlation Matrix Heatmap...")
        plt.figure(figsize=(20, 18))
        # Calculate full correlation matrix
        corr_matrix = numeric_df.corr()
        # Plot heatmap
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", center=0,
                    linewidths=0.5, square=True, cbar_kws={"shrink": .5}, annot_kws={"size": 8})
        plt.title('Correlation Matrix of All Metrics', fontsize=16)
        plt.tight_layout()
        plt.savefig(os.path.join(RESULT_DIR, 'correlation_matrix_heatmap.png'))
        print(f"Saved '{RESULT_DIR}/correlation_matrix_heatmap.png'")
        plt.close()
    
    # Save Sorted Data
    df.to_csv(os.path.join(STAT_DIR, 'sorted_analyzed_data.csv'), index=False)
    
    # 5. Visualization (All Metrics)
    print("\n--- Generating Plots for All Metrics ---")
    sns.set(style="whitegrid")
    
    # Get all metrics except DASS-21 and Severity
    metrics_to_plot = [col for col in HEADERS if col != 'DASS-21' and col in df.columns]
    
    # Configuration for subplots
    cols_per_fig = 3
    rows_per_fig = 3
    plots_per_fig = cols_per_fig * rows_per_fig
    num_figures = math.ceil(len(metrics_to_plot) / plots_per_fig)
    
    for fig_idx in range(num_figures):
        start_idx = fig_idx * plots_per_fig
        end_idx = min((fig_idx + 1) * plots_per_fig, len(metrics_to_plot))
        current_metrics = metrics_to_plot[start_idx:end_idx]
        
        fig, axes = plt.subplots(rows_per_fig, cols_per_fig, figsize=(18, 15))
        axes = axes.flatten()
        
        for i, col in enumerate(current_metrics):
            # Scatter plot with regression line
            sns.scatterplot(data=df, x='DASS-21', y=col, hue='Severity', 
                            hue_order=severity_order, palette='viridis', 
                            ax=axes[i], s=80)
            
            # Add regression line (without hue)
            sns.regplot(data=df, x='DASS-21', y=col, scatter=False, 
                        ax=axes[i], color='red', line_kws={'alpha':0.5})
            
            axes[i].set_title(f'{col} vs DASS-21', fontsize=10, fontweight='bold')
            # Only show legend on the first plot to avoid clutter, or manage it better
            if i == 0:
                axes[i].legend(loc='upper right', title='Severity', fontsize='small')
            else:
                if axes[i].get_legend():
                    axes[i].get_legend().remove()

        # Hide empty subplots
        for j in range(len(current_metrics), len(axes)):
            axes[j].axis('off')
            
        plt.tight_layout()
        output_file = os.path.join(RESULT_DIR, f'analysis_plots_part_{fig_idx + 1}.png')
        plt.savefig(output_file)
        print(f"Saved '{output_file}'")
        plt.close()

    # 6. Grouped Statistics
    print("\n--- Calculating Grouped Statistics ---")
    # Calculate mean and std for each metric grouped by Severity
    # We use numeric_only=True to avoid errors if there are non-numeric columns
    grouped_stats = df.groupby('Severity')[metrics_to_plot].agg(['mean', 'std']).transpose()
    grouped_stats.to_csv(os.path.join(STAT_DIR, 'grouped_statistics.csv'))
    print(f"Grouped statistics saved to '{STAT_DIR}/grouped_statistics.csv'")

    # 7. Box Plots (Distribution Analysis)
    print("\n--- Generating Box Plots ---")
    
    for fig_idx in range(num_figures):
        start_idx = fig_idx * plots_per_fig
        end_idx = min((fig_idx + 1) * plots_per_fig, len(metrics_to_plot))
        current_metrics = metrics_to_plot[start_idx:end_idx]
        
        fig, axes = plt.subplots(rows_per_fig, cols_per_fig, figsize=(18, 15))
        axes = axes.flatten()
        
        for i, col in enumerate(current_metrics):
            sns.boxplot(data=df, x='Severity', y=col, order=severity_order, palette='viridis', ax=axes[i])
            axes[i].set_title(f'{col} Distribution', fontsize=10, fontweight='bold')
            axes[i].set_xlabel('')
            axes[i].tick_params(axis='x', rotation=45)

        # Hide empty subplots
        for j in range(len(current_metrics), len(axes)):
            axes[j].axis('off')
            
        plt.tight_layout()
        output_file = os.path.join(RESULT_DIR, f'box_plots_part_{fig_idx + 1}.png')
        plt.savefig(output_file)
        print(f"Saved '{output_file}'")
        plt.close()

    print("\nAnalysis complete.")

if __name__ == "__main__":
    analyze_raw_data(FILE_NAME)
