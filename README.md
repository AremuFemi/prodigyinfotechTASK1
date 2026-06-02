# 🗺️ Task 1: Global Demographics Analytics Pipeline

## 📌 Project Architecture
This folder handles the automated loading, extraction, filtering, and cross-sectional orchestration of the World Bank Group Global Population database spanning **1960 to 2024**.

## 🛠️ Structural Enhancements Implemented
1. **Double-Counting Remediation:** Programmatically filtered out multi-country macro-aggregates (like "World", "High Income", and "South Asia (IDA & IBRD)") from the core data rows by validating the existence of localized geographic strings in the `Region` key metadata column.
2. **Programmatic Graphical Scaling:** Instead of setting flat visual dimension footprints, the pipeline dynamically calculates y-axis sizing parameters (`max(6, len(region_df) * 0.25)`) across individual sub-regions. This prevents compressed text rendering across densified clusters like Sub-Saharan Africa.
3. **Automated File Formatting:** Strips complex structural notations (commas, spaces, ampersands) to automatically format distinct graphic asset files.

## 📊 Dashboard Access
If you have configured GitHub Pages on your repository root, you can view the complete interactive layout without installing packages locally:
👉 `https://YOUR-GITHUB-USERNAME.github.io/YOUR-REPO-NAME/Task_1_Demographics/index.html`

## 🚀 Execution Baseline
```bash
pip install pandas matplotlib numpy
python task1.py
