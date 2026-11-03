"""Charts (CO5). Every function returns a matplotlib Figure."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def price_distribution(df, title="Listed price distribution"):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(df["listed_price"], bins=30, kde=True, ax=ax)
    ax.set(title=title, xlabel="Listed price (Rs)", ylabel="Listings")
    fig.tight_layout()
    return fig


def brand_comparison(df):
    avg = df.groupby("brand")["listed_price"].mean().sort_values(ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=avg, x="listed_price", y="brand", ax=ax)
    ax.set(title="Average listed price by brand", xlabel="Average price (Rs)", ylabel="")
    fig.tight_layout()
    return fig


def depreciation_curve(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.lineplot(data=df, x="age", y="retained_pct", hue="category",
                 estimator="mean", errorbar=None, marker="o", ax=ax)
    ax.set(title="Value retained vs product age", xlabel="Age (years)",
           ylabel="% of original price retained")
    fig.tight_layout()
    return fig


def verdict_counts(df_analyzed):
    counts = df_analyzed["verdict"].value_counts().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=counts, x="verdict", y="count", ax=ax)
    ax.set(title="Listings by pricing verdict", xlabel="", ylabel="Listings")
    plt.setp(ax.get_xticklabels(), rotation=15)
    fig.tight_layout()
    return fig


def price_vs_age(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.scatterplot(data=df, x="age", y="listed_price", hue="category", alpha=0.6, ax=ax)
    ax.set(title="Listed price vs age", xlabel="Age (years)", ylabel="Listed price (Rs)")
    fig.tight_layout()
    return fig


def comparison_chart(comparable_prices, listed, fair):
    fig, ax = plt.subplots(figsize=(7, 3.5))
    sns.histplot(comparable_prices, bins=12, ax=ax, color="lightgray")
    ax.axvline(listed, color="red", linestyle="--", label=f"Asking Rs {listed:,.0f}")
    ax.axvline(fair, color="green", linestyle="-", label=f"Fair Rs {fair:,.0f}")
    ax.legend()
    ax.set(title="Asking price vs comparable listings", xlabel="Price (Rs)")
    fig.tight_layout()
    return fig
