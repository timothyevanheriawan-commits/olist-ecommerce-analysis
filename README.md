# Olist E-Commerce: Sales & Delivery Performance Analysis

An analysis of approximately **99,441 orders** from the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), covering 2016 to 2018.

The analysis focuses on three business questions:

1. Which product categories contribute the most revenue?
2. How strongly does delivery performance relate to customer satisfaction?
3. Which regions and operational factors should be prioritized for improvement?

**📊 [View the live interactive dashboard](https://olist-commerce-analysis.streamlit.app/)**

**This notebook has been executed end-to-end against the real dataset.** All figures reported below are taken directly from the notebook's actual output.

## Links

* 📊 **Live dashboard:** [olist-commerce-analysis.streamlit.app](https://olist-commerce-analysis.streamlit.app/)
* 📓 **Full analysis:** [`olist_analysis.ipynb`](./olist_analysis.ipynb)
* 📈 **Chart exports:** [`charts/`](./charts/)

## Key Findings

### 1. Revenue is concentrated, but not extremely so

**17 of 72 product categories account for approximately 80% of total revenue.**

The three largest categories are:

| Category          | Share of Revenue |
| ----------------- | ---------------: |
| Health & Beauty   |             9.3% |
| Watches & Gifts   |             8.9% |
| Bed, Bath & Table |             7.6% |

Together, these three categories contribute approximately **24% of total revenue**.

**Business implication:** Delivery-performance improvements should initially focus on high-revenue categories because operational problems in these categories expose more revenue to potential customer dissatisfaction.

---

### 2. Late deliveries are strongly associated with low review scores at the order level

At the order level, delivery delay and review score show a negative Spearman correlation:

**ρ = -0.176, p ≈ 0, n = 95,601**

The difference becomes particularly clear when comparing late and non-late orders:

| Delivery Performance | Average Review Score |
| -------------------- | -------------------: |
| On time / early      |             **4.29** |
| 7+ days late         |             **1.69** |

However, the relationship changes substantially when analyzed at the category level.

Across 63 categories with at least 30 orders:

**ρ = -0.096, p = 0.455**

This category-level result is not statistically significant.

The contrast suggests that the relationship is primarily driven by **individual orders experiencing delays**, rather than certain product categories being structurally slower and receiving worse reviews.

**Business implication:** Improve delivery reliability at the order and logistics level, particularly through carrier performance and delivery-estimate accuracy, rather than treating specific product categories as inherently problematic.

---

### 3. Regional delivery buffers vary substantially

Every state in the regional analysis delivered earlier than the estimated delivery date on average, but the size of that buffer varies considerably.

| State          | Delivery Buffer | Average Review |
| -------------- | --------------: | -------------: |
| Alagoas (AL)   |       -8.8 days |           3.86 |
| São Paulo (SP) |      -11.1 days |           4.25 |
| Acre (AC)      |       ~-20 days |           ~4.1 |
| Rondônia (RO)  |       ~-21 days |           ~4.2 |

São Paulo is by far the highest-volume market with **40,068 orders**, while Alagoas has the smallest average delivery buffer and the lowest average review score among the states shown.

**Business implication:** States with thinner delivery buffers, particularly AL, MA, and SE, may benefit from recalibrated delivery estimates. Smaller buffers leave less room for operational disruptions before an order becomes late.

---

### 4. Freight cost has a negligible relationship with review score

Freight cost as a percentage of order value has an extremely weak negative relationship with review score:

**ρ = -0.031, p = 1.68e-21, n ≈ 94,000**

Although the relationship is statistically significant because of the large sample size, the effect size is extremely small.

This is an important distinction between **statistical significance and practical significance**.

**Business implication:** Freight cost should be deprioritized as a customer-satisfaction lever compared with delivery reliability and delivery-estimate accuracy.

---

### 5. Marketplace growth affects the interpretation of monthly order trends

Raw monthly order volume increases over the 2016 to 2018 period, but this does not necessarily represent seasonal demand.

Olist's marketplace was also growing during this period, meaning that simply comparing monthly order counts can mix **seasonality with overall marketplace expansion**.

The analysis therefore includes an additional view based on **orders per active seller** to provide a more growth-adjusted perspective.

**Business implication:** Seasonal demand should be evaluated relative to marketplace scale rather than using raw order volume alone. This helps distinguish genuine seasonal patterns from growth in the underlying seller base.

---

## Overall Recommendation

The analysis suggests three practical priorities:

### 1. Improve delivery reliability

The strongest customer-satisfaction signal is the relationship between individual delivery delays and review scores.

Focus on:

* Carrier reliability
* Delivery SLA monitoring
* Delivery-estimate accuracy
* Early identification of orders at risk of becoming late

### 2. Recalibrate delivery estimates in thin-buffer regions

States with smaller delivery buffers have less room to absorb operational disruptions.

Review and recalibrate delivery estimates in regions such as **AL, MA, and SE** before applying broad changes across the entire marketplace.

### 3. Deprioritize freight cost as a primary satisfaction lever

The relationship between freight cost and review score is too small to justify prioritizing it over delivery reliability.

The data supports addressing **when an order arrives** before focusing heavily on **how much shipping costs**.

## Methodology

The analysis was performed using a combination of **DuckDB SQL and Python/Pandas**.

1. Raw Olist CSV files were loaded directly using DuckDB.
2. Orders, order items, products, customers, reviews, and payments were cleaned and joined.
3. Item-level data was explicitly aggregated to the order level before order-level joins to avoid duplication caused by the one-to-many relationship between orders and order items.
4. Revenue was analyzed by product category using Pareto analysis.
5. Delivery delay was compared with review scores at both the order and category levels.
6. Regional delivery performance was evaluated after filtering states with insufficient order volume.
7. Monthly order trends were examined alongside a growth-adjusted orders-per-active-seller measure.
8. Payment behavior and freight cost were also evaluated.
9. **Spearman correlation** was used rather than Pearson correlation because review score is an ordinal variable.
10. Aggregated results were exported for use in the Streamlit dashboard.

## Dataset

The analysis uses approximately **99,441 orders** from Olist's Brazilian E-Commerce Public Dataset, covering **2016 to 2018**.

The dataset contains information about:

* Orders
* Order items
* Products
* Customers
* Sellers
* Reviews
* Payments
* Delivery dates
* Product categories
* Brazilian geographic regions

## Limitations

* **1.2% of rows** used in the delay-vs-review analysis were dropped due to missing delay or review-score values: 1,114 of 96,715 observations.
* The **7+ day late** threshold is illustrative rather than a validated SLA threshold. It should be treated as a sensitivity check rather than a formal operational standard.
* **Roraima (RR)** was excluded from the regional analysis because it had fewer than 50 orders.
* `primary_category` represents the category of an order's highest-value item. For multi-category orders, this is therefore an analytical simplification rather than a strict order-level category.
* Category-level correlation was included to test whether product category could explain the order-level delay and review relationship. Both levels are reported rather than relying only on the aggregate correlation.
* Monthly order volume is influenced by Olist marketplace growth as well as seasonal demand. The analysis therefore includes orders per active seller as a complementary growth-adjusted measure.
* Correlation indicates association rather than causation. The observed relationship between delivery delays and review scores should not be interpreted as proof that delays alone caused lower ratings.

## Tech Stack

* **Python**
* **DuckDB** for SQL-based data analysis
* **Pandas / NumPy** for data processing
* **Plotly** for visualization
* **Streamlit** for the interactive dashboard

## Running Locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

## Repository Structure

```text
.
├── olist_analysis.ipynb     # Full SQL + Python analysis
├── app.py                   # Streamlit dashboard
├── requirements.txt         # Python dependencies
├── config.toml              # Dashboard theme configuration
├── data/
│   ├── revenue_by_category.csv
│   ├── delay_review.csv
│   ├── category_delay_review.csv
│   ├── state_delay.csv
│   ├── monthly_orders.csv
│   ├── payment_summary.csv
│   └── delay_review_freight.csv
├── charts/                  # PNG exports of notebook charts
└── README.md
```

## Project Goal

This project demonstrates an end-to-end approach to **e-commerce business analysis**, combining SQL, statistical analysis, data visualization, business interpretation, and an interactive deployed dashboard.

Rather than focusing only on descriptive metrics, the analysis connects operational performance with customer satisfaction and translates the results into **prioritized business recommendations**.
