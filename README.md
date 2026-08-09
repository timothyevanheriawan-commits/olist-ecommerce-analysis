# Olist E-Commerce: Sales & Delivery Performance Analysis

Analysis of ~100k orders from the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
(2016–2018), focused on what drives late deliveries and low review scores, and
which product categories/regions should be prioritized first.

## Links

- 📓 **Kaggle Notebook (full analysis):** [add link once published]
- 📊 **Live dashboard (Streamlit):** [add link once deployed]
- ✍️ **Written case study:** [add link to blog/portfolio post]

## Structure

```
.
├── olist_analysis.ipynb     # full SQL (DuckDB) + pandas analysis, also published on Kaggle
├── app.py                   # Streamlit dashboard (custom theme + CSS)
├── requirements.txt
├── .streamlit/config.toml   # dashboard color theme
├── data/                    # aggregated CSVs exported from the notebook, used by app.py
│   ├── revenue_by_category.csv
│   ├── delay_review.csv
│   ├── category_delay_review.csv
│   ├── state_delay.csv
│   ├── monthly_orders.csv
│   ├── payment_summary.csv
│   └── delay_review_freight.csv
└── README.md
```

## Method

1. Loaded raw Olist CSVs directly with SQL via DuckDB (no database server needed).
2. Cleaned and joined orders, order items, products, customers, reviews, and payments |
   explicitly aggregating item-grain data to order-grain before any order-level join
   (the raw dataset's `order_items` table is one row per item, not per order).
3. Analyzed revenue by category (Pareto), delivery delay vs. review score at both the
   order level and category level (to check for confounding | see Limitations), regional
   delivery performance (filtered to states with sufficient order volume), growth-adjusted
   seasonality, payment type behavior, and freight cost vs. review score.
4. Used Spearman (not Pearson) correlation throughout, since review score is ordinal.
5. Exported aggregated results and built a custom-themed interactive dashboard in Streamlit.

## Key Findings

_(fill in once analysis is finalized | 3-4 findings, each ending in a concrete recommendation)_

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Limitations

- Category-level correlation is included specifically to check whether product category
  confounds the order-level delay-vs-review relationship | report both numbers, not just one.
- States with fewer than 50 orders are excluded from the regional chart as statistically unreliable.
- Raw monthly order volume is influenced by Olist's own marketplace growth in 2016-2018,
  not just seasonal demand | the dashboard includes a growth-adjusted view for this reason.
- The "7+ days late" cutoff used in headline metrics is illustrative, not a validated SLA
  threshold, and should be treated as a sensitivity check rather than a fixed rule.
- _(add: % of rows dropped by dropna, from the notebook's printed output)_
