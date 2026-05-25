import streamlit as st
import pandas as pd
import pickle
import re
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Scam Detection System",
    page_icon="🛡️",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.main {
    background-color: #f4f7fc;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

.hero-section {
    background: linear-gradient(135deg,#2563eb,#06b6d4);
    padding: 60px;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-bottom: 40px;
}

.hero-title {
    font-size: 55px;
    font-weight: bold;
}

.hero-subtitle {
    font-size: 22px;
    margin-top: 15px;
}

.feature-card {
    background-color: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.detect-box {
    background-color: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
}

.dashboard-card {
    background-color: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.06);
    margin-top: 20px;
}

.stButton button {
    width: 100%;
    height: 55px;
    border-radius: 12px;
    border: none;
    background-color: #2563eb;
    color: white;
    font-size: 18px;
    font-weight: bold;
}

.stButton button:hover {
    background-color: #1d4ed8;
    color: white;
}

.result-safe {
    background-color: #dcfce7;
    padding: 25px;
    border-radius: 15px;
    color: #166534;
    font-size: 22px;
    font-weight: bold;
}

.result-scam {
    background-color: #fee2e2;
    padding: 25px;
    border-radius: 15px;
    color: #991b1b;
    font-size: 22px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# =========================================================
# LOAD DATASET
# =========================================================

fraud_data = pd.read_csv("Fraud Dataset.csv")

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero-section">

<div class="hero-title">
🛡️ AI Scam Detection & Fraud Analytics
</div>

<div class="hero-subtitle">
Protect Yourself from OTP Fraud, KYC Scam,
Phishing, Banking Fraud and Online Scams
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# FEATURES SECTION
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
    <h2>📩 Scam Detection</h2>
    <p>Detect spam and scam messages instantly using AI.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
    <h2>📊 Fraud Analytics</h2>
    <p>Visualize fraud trends and targeted locations.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
    <h2>🔐 Cyber Protection</h2>
    <p>Stay protected from phishing and banking scams.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# =========================================================
# DETECTION SECTION
# =========================================================

st.markdown("## 📩 Scam Message Detection")

col1, col2 = st.columns([2,1])

with col1:

    st.markdown('<div class="detect-box">', unsafe_allow_html=True)

    message = st.text_area(
        "Enter suspicious message",
        height=220,
        placeholder="Paste suspicious SMS, email or WhatsApp message here..."
    )

    detect = st.button("Detect Message")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/2092/2092663.png",
        width=300
    )

# =========================================================
# DETECTION LOGIC
# =========================================================

if detect:

    if message.strip() == "":
        st.warning("Please enter a message")

    else:

        # preprocessing
        msg = message.lower()
        msg = re.sub(r'[^\w\s]', '', msg)

        # vectorize
        data = vectorizer.transform([msg])

        # prediction
        prediction = model.predict(data)

        probability = model.predict_proba(data)

        scam_prob = probability[0][1] * 100

        st.write("")
        st.write("")

        # =========================================================
        # RESULT SECTION
        # =========================================================

        st.markdown("## 🔎 Detection Result")

        if prediction[0] == 1:

            st.markdown(f"""
            <div class="result-scam">
            🚨 Scam Message Detected <br><br>
            Confidence: {scam_prob:.2f}%
            </div>
            """, unsafe_allow_html=True)

            st.progress(int(scam_prob))

        else:

            st.markdown(f"""
            <div class="result-safe">
            ✅ Safe Message <br><br>
            Confidence: {100-scam_prob:.2f}%
            </div>
            """, unsafe_allow_html=True)

            st.progress(int(100-scam_prob))

        st.write("")

        # =========================================================
        # ENTERED MESSAGE
        # =========================================================

        st.markdown("### 📄 Entered Message")

        st.info(message)

        # =========================================================
        # SUSPICIOUS KEYWORDS
        # =========================================================

        keywords = [
            "otp",
            "bank",
            "kyc",
            "winner",
            "lottery",
            "urgent",
            "click",
            "verify",
            "account",
            "money",
            "loan",
            "gift"
        ]

        found = []

        for word in keywords:
            if word in msg:
                found.append(word)

        st.markdown("### ⚠️ Suspicious Keywords")

        if len(found) > 0:
            st.write(found)
        else:
            st.success("No suspicious keywords detected")

# =========================================================
# DASHBOARD SECTION
# =========================================================

st.write("")
st.write("")
st.markdown("## 📊 Fraud Analytics Dashboard")

# =========================================================
# METRICS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Fraud Cases", len(fraud_data))

with col2:
    top_location = fraud_data['location'].mode()[0]
    st.metric("Most Targeted Area", top_location)

with col3:
    top_fraud = fraud_data['fraud_type'].mode()[0]
    st.metric("Most Common Fraud", top_fraud)

# =========================================================
# GRAPH SECTION
# =========================================================

# ---------------------------------------------------------
# LOCATION GRAPH
# ---------------------------------------------------------

location_counts = fraud_data['location'].value_counts().head(10)

fig1 = px.bar(
    x=location_counts.index,
    y=location_counts.values,
    color=location_counts.values,
    title="Most Targeted Locations"
)

fig1.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title_x=0.3
)

# ---------------------------------------------------------
# FRAUD TYPE GRAPH
# ---------------------------------------------------------

fraud_counts = fraud_data['fraud_type'].value_counts()

fig2 = px.pie(
    values=fraud_counts.values,
    names=fraud_counts.index,
    title="Fraud Type Distribution"
)

fig2.update_layout(
    paper_bgcolor='white',
    title_x=0.3
)

# ---------------------------------------------------------
# AGE GRAPH
# ---------------------------------------------------------

fig3 = px.histogram(
    fraud_data,
    x='customer_age',
    nbins=20,
    title='Customer Age Analysis'
)

fig3.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title_x=0.3
)

# ---------------------------------------------------------
# CARD TYPE GRAPH
# ---------------------------------------------------------

card_counts = fraud_data['card_type'].value_counts()

fig4 = px.bar(
    x=card_counts.index,
    y=card_counts.values,
    color=card_counts.values,
    title='Card Type Fraud Analysis'
)

fig4.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title_x=0.3
)

# =========================================================
# GRAPH LAYOUT
# =========================================================

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.plotly_chart(fig4, use_container_width=True)

# =========================================================
# PURCHASE CATEGORY GRAPH
# =========================================================

purchase_counts = fraud_data['purchase_category'].value_counts()

fig5 = px.bar(
    x=purchase_counts.index,
    y=purchase_counts.values,
    color=purchase_counts.values,
    title="Purchase Category Fraud Analysis"
)

fig5.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title_x=0.3
)

st.plotly_chart(fig5, use_container_width=True)

# =========================================================
# FRAUD AMOUNT ANALYSIS
# =========================================================

fig6 = px.box(
    fraud_data,
    y='amount',
    title="Fraud Amount Distribution"
)

fig6.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title_x=0.3
)

st.plotly_chart(fig6, use_container_width=True)

# =========================================================
# FOOTER
# =========================================================

st.write("")
st.write("---")

st.markdown("""
<center>

<h4>
Developed using Python, Machine Learning, NLP,
Streamlit & Fraud Analytics
</h4>

</center>
""", unsafe_allow_html=True)
