"""
Olist E-Commerce: Sales & Delivery Performance Dashboard
----------------------------------------------------------
Reads the aggregated CSVs exported from olist_analysis.ipynb and
presents them as a styled interactive dashboard.

Deploy: push this repo (including .streamlit/config.toml) to GitHub,
then deploy on https://streamlit.io/cloud (free, connects to GitHub).
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------
# Page config
# -----------------------------------------------------------------
st.set_page_config(
    page_title="Olist E-Commerce Analysis",
    page_icon="📦",
    layout="wide",
)

DATA_DIR = "data"

ACCENT = "#C44E52"
ACCENT_SOFT = "#DD8452"
INK = "#1A1A1A"
MUTED = "#6B6B63"
PAPER = "#FAFAF8"
CARD = "#F0EEE8"
LINE = "#DEDBD1"

CHART_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Georgia, 'Times New Roman', serif", color=INK, size=13),
        paper_bgcolor=PAPER,
        plot_bgcolor=PAPER,
        colorway=[ACCENT, "#4C72B0", ACCENT_SOFT, "#55A868", "#8172B2"],
        title=dict(font=dict(size=16, family="Georgia, serif")),
        xaxis=dict(gridcolor=LINE, zeroline=False, linecolor=LINE),
        yaxis=dict(gridcolor=LINE, zeroline=False, linecolor=LINE),
        margin=dict(l=10, r=10, t=50, b=10),
    )
)

# -----------------------------------------------------------------
# Custom CSS. Forces the light theme directly instead of depending
# on .streamlit/config.toml, and sets explicit text colors on every
# element so nothing inherits an invisible color from a dark default.
# -----------------------------------------------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Georgia&family=Inter:wght@400;500;600;700&display=swap');

    :root {{
        --background-color: {PAPER};
        --secondary-background-color: {CARD};
        --text-color: {INK};
        --primary-color: {ACCENT};
    }}

    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stMain"],
    [class*="css"] {{
        background-color: {PAPER} !important;
        color: {INK} !important;
        font-family: 'Inter', -apple-system, sans-serif;
    }}

    p, span, li, label, div, a, .stMarkdown, .stMarkdown p {{
        color: {INK};
    }}

    .block-container {{
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }}

    /* --- Page title --- */
    h1 {{
        font-family: Georgia, 'Times New Roman', serif !important;
        font-weight: 400 !important;
        font-size: 2.5rem !important;
        letter-spacing: -0.02em;
        color: {INK} !important;
        margin-bottom: 0.3rem !important;
    }}

    .subtitle {{
        color: {MUTED} !important;
        font-size: 0.95rem;
        padding-bottom: 1.5rem;
        margin-bottom: 2rem;
        border-bottom: 3px solid {INK};
    }}

    .subtitle a {{
        color: {ACCENT} !important;
        text-decoration: none;
        border-bottom: 1px solid {ACCENT};
    }}

    /* --- Section headings, redesigned as one cohesive block --- */
    .section-block {{
        margin-top: 3.5rem;
        margin-bottom: 1.25rem;
    }}

    .section-eyebrow {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        color: {ACCENT} !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }}

    .section-eyebrow::after {{
        content: "";
        flex: 1;
        height: 1px;
        background-color: {LINE};
    }}

    h2.section-title {{
        font-family: Georgia, 'Times New Roman', serif !important;
        font-weight: 400 !important;
        font-size: 1.7rem !important;
        color: {INK} !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.25;
    }}

    .plain-explainer {{
        color: {INK} !important;
        font-size: 0.95rem;
        line-height: 1.55;
        background-color: {CARD};
        border-radius: 4px;
        padding: 0.85rem 1.1rem;
        margin: 0.75rem 0 1.25rem 0;
    }}

    div[data-testid="stMetric"] {{
        background-color: {CARD} !important;
        border: 1px solid {LINE};
        border-left: 3px solid {ACCENT};
        border-radius: 2px;
        padding: 1rem 1.2rem;
    }}

    div[data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] * {{
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {MUTED} !important;
    }}

    div[data-testid="stMetricValue"], div[data-testid="stMetricValue"] * {{
        font-family: Georgia, serif;
        color: {INK} !important;
    }}

    .finding-box {{
        background-color: {CARD} !important;
        border-left: 3px solid {ACCENT};
        padding: 1.1rem 1.4rem;
        margin: 1rem 0 1.5rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
        color: {INK} !important;
    }}

    .finding-box, .finding-box p, .finding-box i, .finding-box span {{
        color: {INK} !important;
    }}

    .finding-box b {{
        color: {ACCENT} !important;
    }}

    .caveat {{
        color: {MUTED} !important;
        font-size: 0.82rem;
        font-style: italic;
        margin-top: -0.5rem;
    }}

    hr {{
        border: none;
        border-top: 1px solid {LINE};
        margin: 2.5rem 0;
    }}

    .stSlider > div > div {{
        color: {ACCENT};
    }}

    button[data-baseweb="tab"] p, .stRadio label p {{
        color: {INK} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def section(number: str, label: str, title: str):
    """Render a section number, eyebrow rule, and heading as one visual unit."""
    st.markdown(
        f"""
        <div class="section-block">
            <div class="section-eyebrow"><span>{number}</span><span>{label}</span></div>
            <h2 class="section-title">{title}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )


def explainer(text: str):
    st.markdown(f'<div class="plain-explainer">{text}</div>', unsafe_allow_html=True)


def caveat(text: str):
    st.markdown(f'<p class="caveat">{text}</p>', unsafe_allow_html=True)


@st.cache_data
def load_data():
    return {
        "revenue_by_category": pd.read_csv(f"{DATA_DIR}/revenue_by_category.csv"),
        "delay_review": pd.read_csv(f"{DATA_DIR}/delay_review.csv"),
        "category_delay_review": pd.read_csv(f"{DATA_DIR}/category_delay_review.csv"),
        "state_delay": pd.read_csv(f"{DATA_DIR}/state_delay.csv"),
        "monthly_orders": pd.read_csv(f"{DATA_DIR}/monthly_orders.csv"),
        "payment_summary": pd.read_csv(f"{DATA_DIR}/payment_summary.csv"),
        "delay_review_freight": pd.read_csv(f"{DATA_DIR}/delay_review_freight.csv"),
    }


data = load_data()
revenue_by_category = data["revenue_by_category"]
delay_review = data["delay_review"]
category_delay_review = data["category_delay_review"]
state_delay = data["state_delay"]
monthly_orders = data["monthly_orders"]
payment_summary = data["payment_summary"]
delay_review_freight = data["delay_review_freight"]

# -----------------------------------------------------------------
# Header
# -----------------------------------------------------------------
st.title("Olist E-Commerce: Sales & Delivery Performance")
st.markdown(
    """
    <div class="subtitle">
    Analysis of roughly 100,000 orders (2016 to 2018) from the
    <a href="https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce">
    Brazilian E-Commerce Public Dataset by Olist</a>.
    Notebook: <i>[add Kaggle link]</i> · Code: <i>[add GitHub link]</i>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------
# Top-line metrics
# -----------------------------------------------------------------
avg_review = delay_review["review_score"].mean()
on_time_share = (delay_review["delivery_delay_days"] <= 0).mean()
late_avg_score = delay_review.loc[delay_review["delivery_delay_days"] > 7, "review_score"].mean()
on_time_avg_score = delay_review.loc[delay_review["delivery_delay_days"] <= 0, "review_score"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg. Review Score", f"{avg_review:.2f} / 5")
col2.metric("On Time or Early", f"{on_time_share:.0%}")
col3.metric("Score, On Time", f"{on_time_avg_score:.2f}")
col4.metric("Score, 7+ Days Late", f"{late_avg_score:.2f}", delta=f"{late_avg_score - on_time_avg_score:.2f}")

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------------
# Section 1: Revenue by category
# -----------------------------------------------------------------
section("01", "Category Mix", "Revenue by Product Category")
explainer(
    "Which product categories bring in the most money? A small number of categories usually "
    "generate most of the revenue, so knowing which ones matter most helps decide where to focus "
    "inventory, marketing, and attention."
)

top_n = st.slider("Categories to show", 5, 30, 15)
top_categories = revenue_by_category.head(top_n)

fig_revenue = px.bar(
    top_categories,
    x="total_revenue",
    y="category",
    orientation="h",
    labels={"total_revenue": "Total Revenue (BRL)", "category": ""},
    template=CHART_TEMPLATE,
)
fig_revenue.update_layout(yaxis={"categoryorder": "total ascending"}, height=450)
fig_revenue.update_traces(marker_color=ACCENT)
st.plotly_chart(fig_revenue, use_container_width=True)

n_for_80pct = (revenue_by_category["cum_revenue_share"] <= 0.8).sum()
caveat(f"{n_for_80pct} of {len(revenue_by_category)} categories account for roughly 80% of total revenue.")

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------------
# Section 2: Delivery delay vs review score, order-level and category-level
# -----------------------------------------------------------------
section("02", "Delivery & Satisfaction", "Delivery Delay vs. Review Score")
explainer(
    "Does arriving late actually make customers leave worse reviews? The first tab checks this order "
    "by order. The second tab checks it again by product category, because it's possible certain "
    "categories are simply both slower to ship and lower rated, which would make delivery speed look "
    "like the culprit when the product itself is really the issue."
)

tab1, tab2 = st.tabs(["Order-Level", "Category-Level (confounding check)"])

with tab1:
    p01, p99 = delay_review["delivery_delay_days"].quantile([0.01, 0.99])
    delay_review_plot = delay_review[delay_review["delivery_delay_days"].between(p01, p99)]

    fig_delay = px.box(
        delay_review_plot,
        x="review_score",
        y="delivery_delay_days",
        labels={"review_score": "Review Score (1-5)", "delivery_delay_days": "Delay vs. Estimate (days)"},
        template=CHART_TEMPLATE,
        color_discrete_sequence=[ACCENT_SOFT],
    )
    fig_delay.add_hline(y=0, line_dash="dash", line_color=MUTED)
    fig_delay.update_layout(height=420)
    st.plotly_chart(fig_delay, use_container_width=True)
    caveat(
        "A few orders had clearly wrong delivery dates in the raw data. The most extreme ones are "
        "trimmed here so they do not stretch the chart out of proportion."
    )

with tab2:
    fig_cat = px.scatter(
        category_delay_review,
        x="avg_delay",
        y="avg_review",
        size="n_orders",
        hover_name="primary_category",
        labels={"avg_delay": "Avg. Delivery Delay (days)", "avg_review": "Avg. Review Score"},
        template=CHART_TEMPLATE,
        color_discrete_sequence=[ACCENT],
    )
    fig_cat.add_vline(x=0, line_dash="dash", line_color=MUTED)
    fig_cat.update_layout(height=420)
    st.plotly_chart(fig_cat, use_container_width=True)
    caveat(
        "Each bubble is one product category, and a bigger bubble means more orders in that category. "
        "Categories with fewer than 30 orders are left out since there is not enough data to trust "
        "their average."
    )

st.markdown(
    f"""
    <div class="finding-box">
    <b>Finding:</b> orders that arrived on time or early got an average review score of {on_time_avg_score:.2f} out of 5.
    Orders that arrived more than 7 days late averaged only {late_avg_score:.2f}.
    <br><br>
    Update this box with your real numbers once the notebook has run: check whether the category-level
    chart above shows the same pattern, or whether it flattens out. If it flattens, product category,
    not delivery speed alone, explains part of the low scores, and the recommendation should say so.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------------
# Section 3: Regional delivery performance
# -----------------------------------------------------------------
section("03", "Regional Performance", "Delivery Delay by State")
explainer(
    "Are some states consistently getting slower deliveries than others? If a handful of states are "
    "the main source of delay, that points toward a logistics fix, such as a regional warehouse or a "
    "different shipping partner, rather than a company-wide problem."
)

fig_state = px.bar(
    state_delay.sort_values("avg_delay_days", ascending=True),
    x="avg_delay_days",
    y="customer_state",
    orientation="h",
    labels={"avg_delay_days": "Avg. Delay (days)", "customer_state": ""},
    template=CHART_TEMPLATE,
)
fig_state.add_vline(x=0, line_dash="dash", line_color=MUTED)
fig_state.update_traces(marker_color="#55A868")
fig_state.update_layout(height=500)
st.plotly_chart(fig_state, use_container_width=True)
caveat(
    "States with fewer than 50 orders are left out. With that few orders, one or two unlucky "
    "deliveries could make a state look much worse than it really is."
)

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------------
# Section 4: Seasonality
# -----------------------------------------------------------------
section("04", "Seasonality", "Order Volume Over Time")
explainer(
    "Does the business get busier at certain times of year? The catch is that Olist itself was a "
    "young, fast-growing platform during 2016 to 2018, so raw order counts went up partly just "
    "because more sellers joined, not only because of seasonal shopping habits. The second view below "
    "adjusts for that growth so the seasonal pattern is easier to see on its own."
)

view = st.radio("View", ["Raw order volume", "Growth-adjusted (orders per active seller)"], horizontal=True)

y_col = "n_orders" if view == "Raw order volume" else "orders_per_seller"
fig_monthly = px.line(
    monthly_orders,
    x="month",
    y=y_col,
    markers=True,
    labels={"month": "", y_col: "Orders" if y_col == "n_orders" else "Orders / Active Seller"},
    template=CHART_TEMPLATE,
)
fig_monthly.update_traces(line_color=ACCENT)
fig_monthly.update_layout(height=400)
st.plotly_chart(fig_monthly, use_container_width=True)
caveat(
    "If you are trying to plan for busy months ahead, use the growth-adjusted view. The raw view mixes "
    "in platform growth, which would overstate how seasonal the business really is."
)

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------------
# Section 5: Payment type and freight
# -----------------------------------------------------------------
section("05", "Payments & Freight", "Payment Behavior & Shipping Cost")
explainer(
    "Two questions here. On the left: do customers spend more when paying by credit card compared to "
    "other methods? On the right: does a high shipping cost, relative to what they bought, make people "
    "leave a worse review, separately from how late the package was?"
)

col1, col2 = st.columns(2)
with col1:
    fig_payment_value = px.bar(
        payment_summary,
        x="payment_type",
        y="avg_value",
        labels={"avg_value": "Avg. Order Value (BRL)", "payment_type": ""},
        template=CHART_TEMPLATE,
    )
    fig_payment_value.update_traces(marker_color="#4C72B0")
    fig_payment_value.update_layout(height=350)
    st.plotly_chart(fig_payment_value, use_container_width=True)

with col2:
    sample_n = min(3000, len(delay_review_freight))
    fig_freight = px.scatter(
        delay_review_freight.sample(sample_n, random_state=1),
        x="freight_pct_of_order",
        y="review_score",
        opacity=0.3,
        labels={"freight_pct_of_order": "Freight as % of Order Value", "review_score": "Review Score"},
        template=CHART_TEMPLATE,
    )
    fig_freight.update_traces(marker_color=ACCENT_SOFT)
    fig_freight.update_layout(height=350)
    st.plotly_chart(fig_freight, use_container_width=True)
    caveat("Showing a random sample of 3,000 orders here so the dots do not overlap into a solid blob.")

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------------
# Recommendation
# -----------------------------------------------------------------
section("06", "Summary", "Recommendation")
st.markdown(
    """
    <div class="finding-box">
    Late deliveries are associated with materially lower review scores, and this pattern holds up
    even after checking it separately by product category, which rules out category alone as the
    explanation. Delivery delay is concentrated in a specific subset of states rather than spread
    evenly across the country, and those states also have enough order volume to justify action.
    <br><br>
    The highest-leverage fix is regional, not company-wide: prioritize carrier renegotiation or a
    regional fulfillment point for the two or three worst-performing, highest-volume states first,
    then re-measure review scores in that region after 60 to 90 days. A company-wide delivery
    initiative would spend the most effort on regions that are not actually driving the problem.
    <br><br>
    <span style="color:#6B6B63; font-style: italic; font-size: 0.85rem;">
    This conclusion is written to match the shape of the analysis above. Swap in your own exact
    figures (correlation values, state names, percentage differences) once you have run the notebook
    end to end, since the wording should follow whatever your real numbers show.
    </span>
    </div>
    """,
    unsafe_allow_html=True,
)