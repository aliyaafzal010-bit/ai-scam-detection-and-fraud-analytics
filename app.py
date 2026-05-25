import streamlit as st
import pandas as pd
import pickle
import re
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Scam Detection",
    page_icon="🛡️",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

body {
    background-color: #f7f9fc;
}

.main {
    background-color: #f7f9fc;
}

/* Hide Streamlit Branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main Container */

.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Hero Section */

.hero {
    background: linear-gradient(135deg, #dbeafe, #e0f2fe);
    padding: 50px;
    border-radius: 25px;
    text-align: center;
    margin-bottom: 40px;
    border: 1px solid #cbd5e1;
}

.hero h1 {
    color: #0f172a;
    font-size: 55px;
    font-weight: bold;
}

.hero p {
    color: #334155;
    font-size: 22px;
}

/* Cards */

.card {
    background-color: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.06);
    border: 1px solid #e2e8f0;
}

/* Feature Cards */

.feature-card {
    background-color: white;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
}

.feature-card h3 {
    color: #0f172a;
}

.feature-card p {
    color: #475569;
}

/* Result Cards */

.safe-box {
    background-color: #dcfce7;
    color: #166534;
    padding: 25px;
    border-radius: 15px;
    font-size: 22px;
    font-weight: bold;
    border: 1px solid #bbf7d0;
}

.scam-box {
    background-color: #fee2e2;
    color: #991b1b;
    padding: 25px;
    border-radius: 15px;
    font-size: 22px;
    font-weight: bold;
    border: 1px solid #fecaca;
}

/* Buttons */

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

/* Text Area */

textarea {
    border-radius: 15px !important;
    border: 2px solid #cbd5e1 !important;
    color: #0f172a !important;
}

/* Headers */

h1, h2, h3 {
    color: #0f172a !important;
}

/* Metrics */

[data-testid="metric-container"] {
    background-color: white;
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.04);
}

[data-testid="metric-container"] label {
    color: #475569 !important;
}

[data-testid="metric-container"] div {
    color: #0f172a !important;
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
<div class="hero">

<h1>🛡️ AI Scam Detection & Fraud Analytics</h1>

<p>
Detect OTP Fraud, KYC Scam, Phishing,
Banking Fraud and Suspicious Messages using AI
</p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# FEATURE SECTION
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
    <h3>📩 Smart Detection</h3>
    <p>AI-powered scam and spam message detection.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
    <h3>📊 Fraud Analytics</h3>
    <p>Analyze fraud trends and targeted locations.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
    <h3>🔐 Cyber Protection</h3>
    <p>Protect yourself from phishing and online scams.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# =========================================================
# DETECTION SECTION
# =========================================================

st.markdown("## 📩 Scam Message Detection")

st.markdown('<div class="card">', unsafe_allow_html=True)

message = st.text_area(
    "Enter Suspicious Message",
    height=200,
    placeholder="Paste suspicious SMS, Email or WhatsApp message here..."
)

detect = st.button("Detect Message")

st.markdown('</div>', unsafe_allow_html=True)

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

        # vectorization
        data = vectorizer.transform([msg])

        # prediction
        prediction = model.predict(data)

        probability = model.predict_proba(data)

        scam_prob = probability[0][1] * 100

        st.write("")

        # =========================================================
        # RESULT
        # =========================================================

        st.markdown("## 🔎 Detection Result")

        if prediction[0] == 1:

            st.markdown(f"""
            <div class="scam-box">
            🚨 Scam Message Detected <br><br>
            Confidence Score: {scam_prob:.2f}%
            </div>
            """, unsafe_allow_html=True)

            st.progress(int(scam_prob))

        else:

            st.markdown(f"""
            <div class="safe-box">
            ✅ Safe Message <br><br>
            Confidence Score: {100-scam_prob:.2f}%
            </div>
            """, unsafe_allow_html=True)

            st.progress(int(100-scam_prob))

        # =========================================================
        # USER MESSAGE
        # =========================================================

        st.write("")
        st.markdown("### 📄 Entered Message")

        st.info(message)

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
    st.metric(
        "Most Targeted Area",
        fraud_data['location'].mode()[0]
    )

with col3:
    st.metric(
        "Most Common Fraud",
        fraud_data['fraud_type'].mode()[0]
    )

st.write("")

# =========================================================
# LOCATION GRAPH
# =========================================================

location_counts = fraud_data['location'].value_counts().head(10)

fig1 = px.bar(
    x=location_counts.index,
    y=location_counts.values,
    text=location_counts.values,
    title="Most Targeted Locations"
)

fig1.update_layout(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font_color="#0f172a",
    title_font_size=22,
    title_x=0.25
)

# =========================================================
# FRAUD TYPE GRAPH
# =========================================================

fraud_counts = fraud_data['fraud_type'].value_counts()

fig2 = px.pie(
    values=fraud_counts.values,
    names=fraud_counts.index,
    title="Fraud Type Distribution"
)

fig2.update_layout(
    paper_bgcolor="#ffffff",
    font_color="#0f172a",
    title_font_size=22,
    title_x=0.25
)

# =========================================================
# AGE GRAPH
# =========================================================

fig3 = px.histogram(
    fraud_data,
    x='customer_age',
    nbins=20,
    title='Targeted Age Groups'
)

fig3.update_layout(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font_color="#0f172a",
    title_font_size=22,
    title_x=0.25
)

# =========================================================
# CARD TYPE GRAPH
# =========================================================

card_counts = fraud_data['card_type'].value_counts()

fig4 = px.bar(
    x=card_counts.index,
    y=card_counts.values,
    text=card_counts.values,
    title='Card Type Fraud Analysis'
)

fig4.update_layout(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font_color="#0f172a",
    title_font_size=22,
    title_x=0.2
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
    text=purchase_counts.values,
    title="Purchase Category Fraud Analysis"
)

fig5.update_layout(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font_color="#0f172a",
    title_font_size=22,
    title_x=0.2
)

st.plotly_chart(fig5, use_container_width=True)

# =========================================================
# AMOUNT ANALYSIS
# =========================================================

fig6 = px.box(
    fraud_data,
    y='amount',
    title="Fraud Amount Analysis"
)

fig6.update_layout(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font_color="#0f172a",
    title_font_size=22,
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

<h4 style='color:#475569;'>
AI-Powered Scam Detection & Fraud Analytics System
</h4>

</center>
""", unsafe_allow_html=True)
