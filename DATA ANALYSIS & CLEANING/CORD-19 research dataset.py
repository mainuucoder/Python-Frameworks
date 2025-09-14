import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter
import pandas as pd
import streamlit as st

# Load the CSV
df = pd.read_csv("metadata.csv", low_memory=False)

'''
# Show dataset size
print("Shape of dataset:", df.shape)

# Show first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Show column names
print("\nColumn names:")
print(df.columns.tolist())

important_cols = ["title", "abstract", "publish_time", "authors", "journal"]
print(df[important_cols].isna().sum())
print(df.describe())

missing_counts = df.isna().sum().sort_values(ascending=False)
print(missing_counts.head(10))

# Drop rows with missing titles or publication date
df = df.dropna(subset=["title", "publish_time"])

# Convert publish_time to datetime
df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")

# Drop rows where publish_time could not be parsed
df = df.dropna(subset=["publish_time"])

# Fill missing authors and journals
df["authors"] = df["authors"].fillna("Unknown")
df["journal"] = df["journal"].fillna("Unknown")

# Normalize journal names (lowercase, strip spaces)
df["journal"] = df["journal"].astype(str).str.lower().str.strip()

# Fill missing abstracts with empty string
df["abstract"] = df["abstract"].fillna("")


print(df.isna().sum().head(10))   # should show near 0 for important columns
print(df.dtypes)                  # publish_time should now be datetime64

df.to_csv("metadata_cleaned.csv", index=False)
print("Cleaned dataset saved as metadata_cleaned.csv")
print(df.shape)                   # dataset will be slightly smaller after dropping rows
'''
df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
print(df["publish_time"].dtypes)

df["year"] = df["publish_time"].dt.year
print(df["year"].value_counts().sort_index().head(20))


df["abstract_word_count"] = df["abstract"].apply(lambda x: len(str(x).split()))
print(df[["abstract", "abstract_word_count"]].head())


papers_by_year = df["year"].value_counts().sort_index()
print(papers_by_year.head(10))   # first 10 years
print(papers_by_year.tail(10))   # last 10 years

# Plot number of papers per year
plt.figure(figsize=(10,5))
papers_by_year.plot(kind="bar")  # bar chart
plt.title("Publications per Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.show()

# 2. Identify top journals publishing COVID-19 research
top_journals = df["journal"].value_counts().head(10)  # top 10 journals by count
print(top_journals)

# Plot top journals
top_journals.sort_values().plot(kind="barh", figsize=(8,6))  # horizontal bar chart
plt.title("Top 10 Journals by Number of Publications")
plt.xlabel("Number of Papers")
plt.ylabel("Journal")
plt.show()

# 3. Find most frequent words in titles (simple word frequency)
# Combine all titles into one long lowercase string
all_titles = " ".join(df["title"].dropna().astype(str).str.lower())

# Extract words: only letters, at least 3 characters
words = re.findall(r"\b[a-z]{3,}\b", all_titles)

# Define common stopwords to ignore
stopwords = {
    "the","and","for","with","from","that","this","covid","covid19",
    "using","study","based","analysis","data","novel","coronavirus"
}

# Filter words: remove stopwords
filtered_words = [w for w in words if w not in stopwords]

# Count top 15 most frequent words
word_counts = Counter(filtered_words).most_common(15)
print(word_counts)

# Plot top words
words, counts = zip(*word_counts)
plt.figure(figsize=(10,5))
plt.bar(words, counts)
plt.title("Most Frequent Words in Paper Titles")
plt.xticks(rotation=45)  # rotate x-axis labels for readability
plt.ylabel("Frequency")
plt.show()











