import streamlit as st
import pandas as pd
import pickle
import re
import matplotlib.pyplot as plt

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="AI Scam Detection System",
    page_icon="🛡️",
    layout="wide"
)

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

h1, h2, h3 {
    color: #111827;
}

.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    border: none;
}

.stButton button:hover {
    background-color: #1e40af;
    color: white;
}

.stTextArea textarea {
    border-radius: 12px;
    border: 2px solid #cbd5e1;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    text-align: center;
}

.hero {
    background: linear-gradient(to right, #2563eb, #06b6d4);
    padding: 50px;
    border-radius: 20px;
    color: white;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD MODEL
# ======================================================

model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# ======================================================
# LOAD DATASET
# ======================================================

fraud_data = pd.read_csv("Fraud Dataset.csv")

# ======================================================
# HERO SECTION
# ======================================================

st.markdown("""
<div class="hero">

<h1>🛡️ AI Scam Detection & Fraud Analytics</h1>

<h4>
Protect Yourself from OTP Fraud, KYC Scam, Phishing,
Lottery Fraud and Banking Scams
</h4>

</div>
""", unsafe_allow_html=True)

st.write("")

# ======================================================
# FEATURES SECTION
# ======================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
    <h3>📩 Scam Detection</h3>
    <p>Detect fraudulent and spam messages instantly.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
    <h3>📊 Fraud Analytics</h3>
    <p>Visualize fraud trends and targeted groups.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
    <h3>🔐 Cyber Protection</h3>
    <p>Stay protected from phishing and cyber scams.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# ======================================================
# DETECTION SECTION
# ======================================================

st.header("📩 Scam Message Detection")

col1, col2 = st.columns([2,1])

with col1:

    message = st.text_area(
        "Enter Message",
        height=180,
        placeholder="Paste suspicious SMS, email or WhatsApp message here..."
    )

    detect = st.button("Detect Message")

with col2:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/2092/2092663.png",
        width=220
    )

# ======================================================
# PREDICTION
# ======================================================

if detect:

    if message.strip() == "":

        st.warning("⚠️ Please enter a message")

    else:

        # preprocessing
        msg = message.lower()
        msg = re.sub(r'[^\w\s]', '', msg)

        # vectorization
        data = vectorizer.transform([msg])

        # prediction
        prediction = model.predict(data)

        # probability
        probability = model.predict_proba(data)

        scam_prob = probability[0][1] * 100

        st.write("")

        # ======================================================
        # RESULT SECTION
        # ======================================================

        st.subheader("🔎 Detection Result")

        if prediction[0] == 1:

            st.error(
                f"🚨 Scam Message Detected\n\n"
                f"Confidence: {scam_prob:.2f}%"
            )

            st.progress(int(scam_prob))

        else:

            st.success(
                f"✅ Safe Message\n\n"
                f"Confidence: {100-scam_prob:.2f}%"
            )

            st.progress(int(100-scam_prob))

        # ======================================================
        # USER MESSAGE
        # ======================================================

        st.subheader("📄 Entered Message")

        st.info(message)

        # ======================================================
        # KEYWORDS
        # ======================================================

        scam_keywords = [
            "otp",
            "bank",
            "verify",
            "lottery",
            "winner",
            "click",
            "urgent",
            "kyc",
            "offer",
            "prize",
            "money",
            "loan"
        ]

        found = []

        for word in scam_keywords:
            if word in msg:
                found.append(word)

        st.subheader("⚠️ Suspicious Keywords")

        if len(found) > 0:
            st.write(found)
        else:
            st.write("No suspicious keywords detected")

# ======================================================
# DASHBOARD SECTION
# ======================================================

st.write("")
st.write("")
st.header("📊 Fraud Analytics Dashboard")

# ======================================================
# METRICS
# ======================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Fraud Cases", len(fraud_data))

with col2:

    if 'State' in fraud_data.columns:
        top_state = fraud_data['State'].mode()[0]
        st.metric("Most Targeted State", top_state)

with col3:

    if 'Age' in fraud_data.columns:
        top_age = fraud_data['Age'].mode()[0]
        st.metric("Most Affected Age", top_age)

st.write("")

# ======================================================
# AGE GRAPH
# ======================================================

if 'Age' in fraud_data.columns:

    st.subheader("👥 Fraud Cases by Age Group")

    age_counts = fraud_data['Age'].value_counts()

    st.bar_chart(age_counts)

# ======================================================
# STATE GRAPH
# ======================================================

if 'State' in fraud_data.columns:

    st.subheader("📍 State Wise Fraud Cases")

    state_counts = fraud_data['State'].value_counts()

    st.bar_chart(state_counts)

# ======================================================
# FRAUD TYPE GRAPH
# ======================================================

if 'Fraud_Type' in fraud_data.columns:

    st.subheader("🚨 Fraud Type Distribution")

    fraud_counts = fraud_data['Fraud_Type'].value_counts()

    fig, ax = plt.subplots()

    ax.pie(
        fraud_counts,
        labels=fraud_counts.index,
        autopct='%1.1f%%'
    )

    st.pyplot(fig)

# ======================================================
# GENDER GRAPH
# ======================================================

if 'Gender' in fraud_data.columns:

    st.subheader("⚧ Gender Wise Fraud Cases")

    gender_counts = fraud_data['Gender'].value_counts()

    st.bar_chart(gender_counts)

# ======================================================
# DATA PREVIEW
# ======================================================

st.subheader("📄 Fraud Dataset Preview")

st.dataframe(fraud_data.head())

# ======================================================
# FOOTER
# ======================================================

st.write("---")

st.markdown("""
<center>

Developed using Python, Streamlit, Machine Learning, NLP & Fraud Analytics

</center>
""", unsafe_allow_html=True)
