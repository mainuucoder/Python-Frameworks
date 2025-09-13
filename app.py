import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="CORD-19 Research Explorer",
    page_icon="🧾",
    layout="wide"
)
st.header("About")
st.info("""
This simple app lets you explore the COVID-19 research dataset.  
You can filter papers by year, look at top journals, and see frequent words in titles.
""")


# ------------------ Load Data ------------------
@st.cache_data
def load_data(path="metadata_cleaned.csv"):
    df = pd.read_csv(path)
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    df["year"] = pd.to_datetime(df["publish_time"], errors="coerce").dt.year.astype('Int64')
    df["abstract_word_count"] = df["abstract"].apply(lambda x: len(str(x).split()))
    df["title_length"] = df["title"].apply(lambda x: len(str(x).split()))
    df["journal"] = df["journal"].astype(str).str.lower().str.strip()
    df["authors"] = df["authors"].fillna("Unknown")
    df["abstract"] = df["abstract"].fillna("")
    return df
# After loading data


df = load_data()

## ------------------ Sidebar Filters ------------------
st.sidebar.header("Data-control")
# Show success message after loading data
st.sidebar.success("Data loaded successfully!")
st.sidebar.header("Filters")

# --- Year Range Slider in Sidebar ---
year_min, year_max = 2015, 2021
selected_year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

# Journal multi-select
top_journals_list = df["journal"].value_counts().head(20).index.tolist()
selected_journals = st.sidebar.multiselect("Select Journals", ["All"] + top_journals_list, default=["All"])

# Keyword search in titles
keyword = st.sidebar.text_input("Search Title Keyword")

# Abstract word count range
min_words, max_words = int(df["abstract_word_count"].min()), int(df["abstract_word_count"].max())

# Title length range filter
min_title, max_title = int(df["title_length"].min()), int(df["title_length"].max())
selected_title_length = st.sidebar.slider("Title Length Range", min_title, max_title, (min_title, max_title))

# Top N display options for charts
top_n_journals = st.sidebar.number_input("Top N Journals to Display", min_value=5, max_value=20, value=10)
top_n_authors = st.sidebar.number_input("Top N Authors to Display", min_value=5, max_value=20, value=10)

# Apply filters
filtered_df = df[
    (df["year"] >= selected_year_range[0]) & (df["year"] <= selected_year_range[1]) &
       (df["title_length"] >= selected_title_length[0]) & (df["title_length"] <= selected_title_length[1])
]
if "All" not in selected_journals:
    filtered_df = filtered_df[filtered_df["journal"].isin_]()

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Publications", "Content Analysis", "Raw Data"])

# ------------------ TAB 1: Overview ------------------

with tab1:
    st.header("📊 Dataset Overview")

    # Calculate publications per year
    papers_by_year = filtered_df["year"].value_counts().sort_index()

    # --- Metrics ---
    total_papers = papers_by_year.sum()
    peak_year = papers_by_year.idxmax()
    peak_count = papers_by_year.max()
    avg_papers = int(papers_by_year.mean())

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Papers", total_papers)
    col2.metric("Peak Year", f"{peak_year} ({peak_count})")
    col3.metric("Average Papers/Year", avg_papers)
    col4.metric("Year Range", f"{papers_by_year.index.min()} - {papers_by_year.index.max()}")

    # --- Line Graph ---
    st.subheader("Publications Over Time (2015-2021)")
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(papers_by_year.index, papers_by_year.values, marker='o', linestyle='-', color='teal')
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Papers")
    ax.set_title("Publications Over Time")
    ax.grid(True)
    st.pyplot(fig)

    # --- Insights ---
    if peak_year >= 2020:
        st.markdown("📈 Noticeable spike in publications starting in 2020, reflecting the surge in COVID-19 research during the pandemic.")
    else:
        st.markdown("📊 Publication numbers are relatively stable over the years.")

# ------------------ TAB 2: Publications ------------------
with tab2:
    st.header("📰 Publications Analysis")
    
    st.subheader("Number of Papers per Year")
    papers_by_year = filtered_df["year"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(12,5))
    sns.barplot(x=papers_by_year.index, y=papers_by_year.values, palette="viridis", ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Papers")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Top Journals")
    top_journals = filtered_df["journal"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x=top_journals.values, y=top_journals.index, palette="magma", ax=ax)
    ax.set_xlabel("Number of Papers")
    ax.set_ylabel("Journal")
    st.pyplot(fig)


# ------------------ TAB 3: Content Analysis ------------------
with tab3:
    st.header("📝 Content Analysis")

    # --- Frequent Words in Titles ---
    st.subheader("Most Frequent Words in Titles")
    all_titles = " ".join(filtered_df["title"].dropna().astype(str).str.lower())
    words = re.findall(r"\b[a-z]{3,}\b", all_titles)
    stopwords = {"the","and","for","with","from","that","this","covid","covid19",
                 "using","study","based","analysis","data","novel","coronavirus"}
    filtered_words = [w for w in words if w not in stopwords]
    word_counts = Counter(filtered_words).most_common(15)

    if word_counts:
        words_list, counts = zip(*word_counts)
        fig, ax = plt.subplots(figsize=(12,5))
        sns.barplot(x=list(words_list), y=list(counts), palette="coolwarm", ax=ax)
        plt.xticks(rotation=45)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    else:
        st.write("No titles available for this selection.")

    # --- Frequent Words in Abstracts ---
    st.subheader("Most Frequent Words in Abstracts")
    all_abstracts = " ".join(filtered_df["abstract"].dropna().astype(str).str.lower())
    words_abstracts = re.findall(r"\b[a-z]{3,}\b", all_abstracts)
    filtered_words_abs = [w for w in words_abstracts if w not in stopwords]
    word_counts_abs = Counter(filtered_words_abs).most_common(15)

    if word_counts_abs:
        words_abs, counts_abs = zip(*word_counts_abs)
        fig, ax = plt.subplots(figsize=(12,5))
        sns.barplot(x=list(words_abs), y=list(counts_abs), palette="viridis", ax=ax)
        plt.xticks(rotation=45)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    else:
        st.write("No abstracts available for this selection.")

    # --- Abstract Word Count Distribution ---
    st.subheader("Abstract Word Count Distribution")
    fig, ax = plt.subplots(figsize=(12,4))
    sns.histplot(filtered_df["abstract_word_count"], bins=30, kde=True, color="skyblue", ax=ax)
    ax.set_xlabel("Word Count")
    ax.set_ylabel("Number of Papers")
    st.pyplot(fig)

    # --- Title Length Distribution ---
    st.subheader("Title Length Distribution")
    fig, ax = plt.subplots(figsize=(12,4))
    sns.histplot(filtered_df["title_length"], bins=20, kde=True, color="salmon", ax=ax)
    ax.set_xlabel("Title Length (words)")
    ax.set_ylabel("Number of Papers")
    st.pyplot(fig)

    # --- Top Authors ---
    st.subheader("Top Authors in Selection")
    top_authors = filtered_df["authors"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=top_authors.values, y=top_authors.index, palette="magma", ax=ax)
    ax.set_xlabel("Number of Papers")
    ax.set_ylabel("Author")
    st.pyplot(fig)


# ------------------ TAB 4: Raw Data ------------------
with tab4:
    st.header("📑 Raw Data Viewer")
    st.dataframe(filtered_df[["title","authors","journal","year","abstract_word_count"]].head(100))
    st.download_button("Download Filtered Data", filtered_df.to_csv(index=False), "filtered_metadata.csv")
