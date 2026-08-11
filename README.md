# Olist E-Commerce: Sales & Delivery Performance Analysis

Analysis of ~99,441 orders from the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
(2016–2018), focused on what drives late deliveries and low review scores, and
which product categories/regions should be prioritized first.

**This notebook has been executed end-to-end against the real dataset.** All numbers below
are copied directly from the notebook's actual output, not estimated or written in advance.

## Links

- 📓 **Notebook (full analysis, executed):** `olist_analysis.ipynb` in this repo
- 📊 **Dashboard (Streamlit):** not yet deployed — run locally with the instructions below
- ✍️ **Written case study:** not yet written — the Key Findings section below is the
  current substitute

## Structure

```
.
├── olist_analysis.ipynb     # full SQL (DuckDB) + pandas analysis — executed, outputs saved
├── app.py                   # Streamlit dashboard (custom theme + CSS)
├── requirements.txt
├── config.toml               # dashboard color theme
├── data/                    # aggregated CSVs exported from the executed notebook, used by app.py
│   ├── revenue_by_category.csv
│   ├── delay_review.csv
│   ├── category_delay_review.csv
│   ├── state_delay.csv
│   ├── monthly_orders.csv
│   ├── payment_summary.csv
│   └── delay_review_freight.csv
├── charts/                  # PNG exports of every chart the notebook produces
└── README.md
```

## Method

1. Loaded raw Olist CSVs directly with SQL via DuckDB (no database server needed).
2. Cleaned and joined orders, order items, products, customers, reviews, and payments —
   explicitly aggregating item-grain data to order-grain before any order-level join
   (the raw dataset's `order_items` table is one row per item, not per order).
3. Analyzed revenue by category (Pareto), delivery delay vs. review score at both the
   order level and category level (to check for confounding — see Limitations), regional
   delivery performance (filtered to states with sufficient order volume), growth-adjusted
   seasonality, payment type behavior, and freight cost vs. review score.
4. Used Spearman (not Pearson) correlation throughout, since review score is ordinal.
5. Exported aggregated results and built a custom-themed interactive dashboard in Streamlit.

## Key Findings

**1. Revenue is concentrated but not extremely so.** 17 of 72 categories account for
~80% of total revenue. The top 3 — health_beauty (9.3%), watches_gifts (8.9%),
bed_bath_table (7.6%) — make up ~24% on their own. **→ Prioritize delivery-performance
fixes for these top categories first; they carry the most revenue risk if delivery
problems drag down reviews.**

**2. Late delivery is strongly linked to bad reviews at the order level — but not at
the category level.** Order-level Spearman correlation between delivery delay and
review score: **ρ = -0.176, p ≈ 0 (n = 95,601)**. Orders delivered 7+ days late average
a **1.69** review score vs. **4.29** for on-time/early orders — a large, highly
significant gap. But re-running the same correlation at the category level (63
categories with ≥30 orders) gives **ρ = -0.096, p = 0.455** — the relationship
weakens sharply and loses significance. This means most of the effect comes from
delay varying *within* categories (an individual late order gets a bad review),
not from certain categories being structurally slower and worse-rated as a group.
**→ Fix delay as an order-level operational problem (carrier SLAs, delivery-estimate
accuracy) — don't target specific "slow categories," the data doesn't support that
being the more effective lever.**

**3. Every state delivers ahead of estimate on average, but the safety margin varies
a lot.** Alagoas (AL) has the thinnest buffer (-8.8 days) and the lowest average
review score in the table (3.86). Acre (AC) and Rondônia (RO) have the largest
buffers (~-20 to -21 days) and healthier review scores (~4.1-4.2). São Paulo (SP) —
by far the highest-volume state at 40,068 orders — sits mid-table (-11.1 days,
4.25 average review). **→ Recalibrate delivery-time estimates specifically for
thin-buffer states (AL, MA, SE) — a small margin means small operational hiccups
are more likely to actually become a late delivery there than elsewhere.**

**4. Freight cost is not a meaningful lever.** Freight-as-%-of-order-value vs.
review score: **ρ = -0.031, p = 1.68e-21**. Statistically significant purely because
of the large sample size (n ≈ 94,000) — the effect size is too small to act on.
**→ Deprioritize freight cost relative to Findings 2 and 3.**

**Overall recommendation:** focus first on delivery-estimate accuracy and carrier
reliability broadly (not category-specific), and second on recalibrating delivery
windows for thin-buffer states — both are where the data shows the strongest,
most defensible signal.

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Limitations

- 1.2% of rows (1,114 of 96,715) were dropped from the delay-vs-review analysis for
  missing delay or review score — small enough not to materially bias the headline
  correlation, disclosed here rather than left silent.
- The "7+ days late" cutoff used in the headline delay comparison is illustrative,
  not a validated SLA threshold — treat it as a sensitivity check, not a fixed rule.
- One state (RR / Roraima) was excluded from the regional analysis for having fewer
  than 50 orders.
- `primary_category` is defined as the category of an order's highest-value item —
  a reasonable simplification for multi-category orders, but it means "category"
  here is a per-order label, not a strict SKU-level category.
- Category-level correlation is included specifically to check whether product
  category confounds the order-level delay-vs-review relationship — both numbers
  are reported above, not just the order-level one.
- Raw monthly order volume is influenced by Olist's own marketplace growth in
  2016–2018, not just seasonal demand — the notebook includes a growth-adjusted
  (orders-per-active-seller) view for this reason, though it hasn't yet been
  distilled into a standalone finding above; that's a natural fifth finding to add.
