import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sentiment Dashboard", layout="wide")
url=st.secrets["url"]

def topbar_ui(username):
    col1, col2 = st.columns([8, 1])
    with col1:
        st.markdown(
            f"<div style='text-align: right; font-weight: bold; font-size: 1.1em;'>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col2:
        if st.button("Logout", key="logout_top"):
            st.session_state.logged_in = False
            st.session_state.user = ""
            st.rerun()

def sentiment_dashboard():
    topbar_ui(st.session_state.user)

    st.markdown("<h1 style='text-align:center;'>Finance Sentiment Dashboard</h1>", unsafe_allow_html=True)

    if "results" not in st.session_state:
        st.session_state.results = pd.DataFrame(columns=["Datetime", "Text", "Sentiment", "Confidence", "Sentiment_Score"])

    input_text = st.text_area("Enter headlines (one per line):", height=100)
    uploaded_file = st.file_uploader("Or upload CSV/Excel with text column", type=['csv', 'xlsx'])
    if st.button("Analyze"):
        with st.spinner("Analyzing..."):
            texts = []
            if input_text.strip():
                texts = [t.strip() for t in input_text.splitlines() if t.strip()]
            elif uploaded_file:
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
                texts = df["text"].dropna().tolist() if "text" in df.columns else []
            else:
                st.warning("Provide input text or upload a file.")
            if texts:
                data={"texts":texts}
                response = requests.post(url, json=data)
                df_new=pd.DataFrame()
                if response.status_code == 200:
                    df_new = df_new.append([response.json()],ignore_index=True)
                st.session_state.results = pd.concat([df_new, st.session_state.results], ignore_index=True)

    results = st.session_state.results

    if not results.empty:
        st.subheader("Recent Analyses")
        st.dataframe(results[["Text", "Sentiment", "Confidence", "Sentiment_Score"]],
                     use_container_width=True, hide_index=True)

        st.subheader("Sentiment Distribution")
        fig_pie = px.pie(results, names="Sentiment", hole=0.4,
                         color_discrete_map={"Positive": "green", "Negative": "red", "Neutral": "gray"})
        st.plotly_chart(fig_pie, use_container_width=True)

        st.subheader("Sentiment Over Time")
        df_time = results.copy()
        df_time["Date"] = pd.to_datetime(df_time["Datetime"]).dt.date
        trend = df_time.groupby(["Date", "Sentiment"]).size().unstack(fill_value=0)
        st.plotly_chart(px.line(trend, x=trend.index, y=trend.columns, markers=True),
                        use_container_width=True)

        st.subheader("Keyword Analysis")
        from sklearn.feature_extraction.text import CountVectorizer
        cv = CountVectorizer(stop_words='english', max_features=20)
        word_matrix = cv.fit_transform(results["Text"])
        keywords = cv.get_feature_names_out()
        counts = word_matrix.sum(axis=0).A1
        score_map = []
        for kw in keywords:
            mask = results["Text"].str.contains(rf"\b{kw}\b", case=False)
            avg = results[mask]["Sentiment_Score"].mean()
            score_map.append("Positive" if avg >= 7 else "Negative" if avg <= 3 else "Neutral")
        df_kw = pd.DataFrame({"Keyword": keywords, "Mentions": counts, "Avg. Sentiment": score_map})
        st.dataframe(df_kw, use_container_width=True)

        st.subheader("Export & Alerts")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("Download CSV", results.to_csv(index=False), "sentiments.csv")
        with col2:
            threshold = st.slider("Alert threshold (%)", 0, 100, 30)
            neg_pct = 100 * results["Sentiment"].str.lower().eq("negative").mean()
            if neg_pct >= threshold:
                st.error(f"Negative sentiment at {neg_pct:.1f}%!")
            else:
                st.success(f"Negative sentiment is {neg_pct:.1f}%")
