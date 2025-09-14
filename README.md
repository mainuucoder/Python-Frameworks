# Python-Frameworks
---

# 🧾 CORD-19 Research Explorer

A **Streamlit web application** for exploring COVID-19 research papers using the **CORD-19 metadata dataset**. This app allows interactive analysis of publications, journals, authors, and paper content.

---

## 🌐 Live App

👉 Try the app here: [CORD-19 Research Explorer]([https://share.streamlit.io/your-username/cord19-research-explorer/main/app.py)](https://mainuu-work.streamlit.app/)



---

## 📂 Dataset

* **File used:** `metadata.csv` from the CORD-19 dataset
* **Columns include:**

  * `title`, `abstract`, `authors`, `journal`, `publish_time`, `year`, etc.
* **Preprocessing:**

  * Convert `publish_time` to `datetime`
  * Extract `year` as integer
  * Calculate `abstract_word_count` and `title_length`
  * Fill missing values for authors and abstracts

---

## ⚙️ Features

### Sidebar Filters

* **✅ Success Message**: Shows “Data loaded successfully!”
* **📅 Year Range Slider**: Filter papers by publication year (2015–2021)
* **📚 Journal Multi-Select**: Choose one or more journals
* **🔍 Keyword Search**: Filter papers by keywords in titles
* **✍️ Abstract Word Count Range**: Filter by abstract length
* **📝 Title Length Range**: Filter by title length
* **📊 Top N Options**: Control number of journals/authors displayed in charts

### Tabs

1. **Overview 📊**

   * Line graph: Publications over time
   * Metrics: Total papers, peak year, average papers/year, year range
   * Insights based on selected filters

2. **Publications 📰**

   * Top journals bar chart
   * Papers per year distribution

3. **Content Analysis 📝**

   * Word frequencies (titles & abstracts)
   * Abstract word count distribution
   * Title length distribution
   * Top authors

4. **Raw Data 📑**

   * Interactive data table
   * Download filtered data as CSV

---

## 🖥️ Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_folder>
```

2. Install dependencies:

```bash
pip install pandas streamlit matplotlib seaborn
```

3. Run the app locally:

```bash
streamlit run app.py
```

---

## 🚀 Deployment

### Deploy on Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Connect your repository
4. Select `app.py` as the entry point
5. Deploy and copy the live app URL

### Deploy on Heroku (Optional)

1. Add a `requirements.txt` file
2. Create a `Procfile` with:

   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
3. Push to Heroku and copy the live app link

---

## 💡 Usage

* Use the **sidebar filters** to refine dataset by year, journal, or keywords
* Explore interactive tabs:

  * **Overview:** Trends & metrics
  * **Publications:** Journals & yearly counts
  * **Content Analysis:** Word usage & distributions
  * **Raw Data:** View/download filtered dataset

---

## ⚡ Key Insights

* Clear **spike in publications starting 2020** due to the COVID-19 pandemic
* Distribution of research across multiple top journals
* Abstract and title length trends provide insight into paper writing patterns

---

## 🎨 Visualization Tools

* **Matplotlib & Seaborn**: Charts and plots
* **Streamlit**: Interactive UI with sidebar, filters, and tabs

---

## 📌 Notes

* Ensure `metadata_cleaned.csv` is placed in the same folder as `app.py`
* App automatically updates graphs & metrics based on filter selections

---

## 👨‍💻 Author

* Developed by **\[DANIEL MUTAHI]**
* For educational use: Beginner-friendly assignment on **data analysis & visualization**

---

