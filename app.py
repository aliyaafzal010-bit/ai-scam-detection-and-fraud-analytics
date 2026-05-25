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

/* Background */

.stApp {
    background-color: #f5f6fb;
}

/* Hide Streamlit */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main Layout */

.block-container {
    padding-top: 1.5rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Hero Section */

.hero {
    background: linear-gradient(135deg, #eef2ff, #f5f3ff);
    padding: 45px;
    border-radius: 30px;
    margin-bottom: 30px;
    border: 1px solid #e2e8f0;
}

.hero h1 {
    color: #1e293b;
    font-size: 52px;
    font-weight: 700;
    text-align: center;
}

.hero p {
    color: #64748b;
    font-size: 20px;
    text-align: center;
}

/* Feature Cards */

.feature-card {
    background-color: white;
    padding: 22px;
    border-radius: 22px;
    text-align: center;
    border: 1px solid #e2e8f0;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.04);
}

.feature-card h3 {
    color: #1e293b;
}

.feature-card p {
    color: #64748b;
}

/* Detection Box */

.detect-box {
    background-color: white;
    padding: 30px;
    border-radius: 25px;
    border: 1px solid #e2e8f0;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.04);
}

/* Result Cards */

.safe-box {
    background: #dcfce7;
    color: #166534;
    padding: 25px;
    border-radius: 18px;
    font-size: 22px;
    font-weight: bold;
}

.scam-box {
    background: #fee2e2;
    color: #991b1b;
    padding: 25px;
    border-radius: 18px;
    font-size: 22px;
    font-weight: bold;
}

/* Button */

.stButton button {
    width: 100%;
    height: 52px;
    background: linear-gradient(135deg, #7c3aed, #6366f1);
    color: white;
    border-radius: 14px;
    border: none;
    font-size: 18px;
    font-weight: 600;
}

.stButton button:hover {
    color: white;
}

/* Text Area */

textarea {
    border-radius: 15px !important;
    border: 2px solid #e2e8f0 !important;
    color: #1e293b !important;
}

/* Metrics */

[data-testid="metric-container"] {
    background-color: white;
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.04);
}

[data-testid="metric-container"] label {
    color: #64748b !important;
}

[data-testid="metric-container"] div {
    color: #1e293b !important;
}

/* Headers */

h1, h2, h3 {
    color: #1e293b !important;
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
Detect OTP Fraud, KYC Scam, Banking Fraud,
Phishing and Online Scam Messages using AI
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
    <p>Visualize fraud trends and targeted groups.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
    <h3>🔐 Cyber Security</h3>
    <p>Protect users from phishing and cyber scams.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# =========================================================
# DETECTION SECTION
# =========================================================

st.markdown("## 📩 Scam Message Detection")

st.markdown('<div class="detect-box">', unsafe_allow_html=True)

message = st.text_area(
    "Enter suspicious message",
    height=180,
    placeholder="Paste suspicious SMS, Email or WhatsApp message..."
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

        msg = message.lower()
        msg = re.sub(r'[^\w\s]', '', msg)

        data = vectorizer.transform([msg])

        prediction = model.predict(data)

        probability = model.predict_proba(data)

        scam_prob = probability[0][1] * 100

        st.write("")
        st.markdown("## 🔎 Detection Result")

        if prediction[0] == 1:

            st.markdown(f"""
            <div class="scam-box">
            🚨 Scam Message Detected <br><br>
            Confidence Score: {scam_prob:.2f}%
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div class="safe-box">
            ✅ Safe Message <br><br>
            Confidence Score: {100-scam_prob:.2f}%
            </div>
            """, unsafe_allow_html=True)

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
    st.metric("Total Cases", len(fraud_data))

with col2:
    st.metric(
        "Top Fraud Area",
        fraud_data['location'].mode()[0]
    )

with col3:
    st.metric(
        "Top Fraud Type",
        fraud_data['fraud_type'].mode()[0]
    )

st.write("")

# =========================================================
# GRAPH 1 - FRAUD TYPE
# =========================================================

fraud_counts = fraud_data['fraud_type'].value_counts()

fig1 = px.pie(
    values=fraud_counts.values,
    names=fraud_counts.index,
    hole=0.5,
    color_discrete_sequence=[
        "#8b5cf6",
        "#6366f1",
        "#60a5fa",
        "#c084fc",
        "#f472b6"
    ]
)

fig1.update_layout(
    title="Fraud Type Distribution",
    height=320,
    paper_bgcolor="#ffffff",
    font_color="#1e293b",
    title_x=0.2
)

# =========================================================
# GRAPH 2 - LOCATION
# =========================================================

location_counts = fraud_data['location'].value_counts().head(6)

fig2 = px.bar(
    x=location_counts.index,
    y=location_counts.values,
    text=location_counts.values,
    color=location_counts.values,
    color_continuous_scale="purples"
)

fig2.update_layout(
    title="Most Targeted Locations",
    height=320,
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font_color="#1e293b",
    coloraxis_showscale=False,
    title_x=0.2
)

# =========================================================
# GRAPH 3 - AGE GROUP
# =========================================================

fig3 = px.histogram(
    fraud_data,
    x="customer_age",
    nbins=15,
    color_discrete_sequence=["#8b5cf6"]
)

fig3.update_layout(
    title="Targeted Age Groups",
    height=320,
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font_color="#1e293b",
    title_x=0.2
)

# =========================================================
# GRAPH 4 - CARD TYPE
# =========================================================

card_counts = fraud_data['card_type'].value_counts()

fig4 = px.bar(
    x=card_counts.index,
    y=card_counts.values,
    text=card_counts.values,
    color=card_counts.values,
    color_continuous_scale="blues"
)

fig4.update_layout(
    title="Card Type Fraud Analysis",
    height=320,
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font_color="#1e293b",
    coloraxis_showscale=False,
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
    color=purchase_counts.values,
    color_continuous_scale="tealgrn"
)

fig5.update_layout(
    title="Purchase Category Fraud Analysis",
    height=320,
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font_color="#1e293b",
    coloraxis_showscale=False,
    title_x=0.2
)

st.plotly_chart(fig5, use_container_width=True)

# =========================================================
# FOOTER
# =========================================================

st.write("")
st.write("---")

st.markdown("""
<center>

<h4 style='color:#64748b;'>
AI Powered Scam Detection & Fraud Analytics System
</h4>

</center>
""", unsafe_allow_html=True)
