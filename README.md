# COMP5541 Group Project — Evaluating and Improving Large Language Model Systems

> **The Hong Kong Polytechnic University · COMP5541 · Summer 2026**

## 📋 Overview

This project presents a systematic framework for evaluating the capabilities of state-of-the-art Large Language Models (LLMs). We design a benchmark dataset spanning five cognitive categories, build an automated evaluation pipeline powered by Claude API, and analyze model performance through quantitative scoring and data visualization.

## 🎯 Evaluation Categories

| # | Category | Description |
|---|----------|-------------|
| 1 | **Complex Logical Deduction** | Multi-constraint spatial logic, propositional logic, epistemic reasoning |
| 2 | **Advanced Mathematical Reasoning** | Proof-based problems, multi-step calculations, abstract algebra |
| 3 | **Semantic Understanding & Inference** | Contextual comprehension, pragmatics, figurative language |
| 4 | **Multi-step Coding & Debugging** | Algorithm design, code debugging, system-level programming |
| 5 | **Domain-specific Knowledge** | Specialized knowledge in science, law, medicine, etc. |

## 🏗️ Project Structure

```
comp5541_project/
├── README.md                           # This file
├── COMP5541_Group_Project_Report.md    # Full project report (Markdown)
├── COMP5541_Group_Project_Report.pdf   # Full project report (PDF)
│
├── eval_pipelines.py                   # Automated LLM evaluation pipeline (Claude API)
├── add_scores.py                       # Score computation for evaluation records
├── autofill.py                         # Auto-fill evaluation data into spreadsheets
├── fill1.py                            # Supplementary data filling utility
├── generate_charts.py                  # Visualization chart generation
├── convert_report.py                   # Markdown → PDF report converter
│
├── records.xlsx                        # Raw evaluation records
├── records_filled.xlsx                 # Evaluation records with filled responses
├── records_final_all_done.xlsx         # Completed evaluation records
├── records_final_with_scores.xlsx      # Final records with computed scores
│
├── chart1_grouped_bar.png              # Grouped bar chart — scores by category
├── chart2_donut_distribution.png       # Donut chart — score distribution
├── chart3_radar.png                    # Radar chart — multi-dimensional comparison
│
└── .gitignore
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- An Anthropic API key (for running the evaluation pipeline)

### Installation

```bash
git clone https://github.com/jas0nShen/comp5541.git
cd comp5541
pip install anthropic openpyxl matplotlib numpy
```

### Usage

#### 1. Run Evaluation Pipeline

```bash
# Set your API key
export ANTHROPIC_API_KEY="your-api-key"

# Run automated evaluation
python eval_pipelines.py
```

#### 2. Compute Scores

```bash
python add_scores.py
```

#### 3. Generate Visualizations

```bash
python generate_charts.py
```

#### 4. Generate PDF Report

```bash
python convert_report.py
```

## 📊 Sample Results

The project evaluates LLM performance across all five categories using a structured rubric. Key outputs include:

- **Grouped Bar Chart** — Comparison of scores across categories
- **Donut Chart** — Distribution of score levels (Excellent / Good / Fair / Poor)
- **Radar Chart** — Multi-dimensional capability profile

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM API | Anthropic Claude API |
| Data Processing | Python, openpyxl |
| Visualization | Matplotlib, NumPy |
| Report Generation | Markdown, WeasyPrint |

## 📄 License

This project is developed for academic purposes as part of the COMP5541 course at The Hong Kong Polytechnic University.

## 👥 Contributors

COMP5541 Group Project Team — Summer 2026
