import streamlit as st
from auth import
def hero():
    st.set_page_config(
        page_title="Finance Sentiment Analysis",
        layout="centered"
    )

    with st.container():
        st.markdown(
        """
        <style>
        .custom-bg {
            background-image: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ02QbF8XEI0ExKgwMWeBBJTtdzfMnlWbSGOD1d_YrdC9A12o1SzVUZ2Yw&s');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            padding: 40px;
            border-radius: 12px;
            color: white;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

        st.markdown(
        """
        <div class="custom-bg">
            <h2>Unlock Financial Market Sentiment</h2>
            <p>Analyze real-time sentiment from news, social media, and financial reports to make smarter investment decisions.</p>
        </div>
        """,
        unsafe_allow_html=True
    ) 
        col1, col2, col3 = st.columns([3, 4, 1])
        with col2:
            if st.button("Get Started"):
                

    st.markdown("---")

    with st.container():
        st.markdown(
            "<h3 style='text-align: center; color:#1f2937;'>Why Choose Our Sentiment Analysis?</h3>",
            unsafe_allow_html=True
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### Real-time Insights")
            st.write("Stay ahead with up-to-the-minute market sentiment.")
        with col2:
            st.markdown("### Multi-source Data")
            st.write("Aggregate news, tweets, and reports in one place.")
        with col3:
            st.markdown("### Actionable Analytics")
            st.write("Transform sentiment into smarter investment strategies.")
