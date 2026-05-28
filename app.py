import streamlit as st
import pandas as pd
import pickle
import re
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Scam Detection & Awareness",
    page_icon="🛡️",
    layout="wide"
)

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
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* =========================================================
BACKGROUND
========================================================= */

.stApp{
    background: linear-gradient(
        135deg,
        #f1f5f9,
        #e2e8f0,
        #e0e7ff
    );
}

/* Hide Streamlit */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Main Padding */

.block-container{
    padding-top:2rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* =========================================================
HERO SECTION
========================================================= */

.hero{
    background:linear-gradient(
        135deg,
        #dbeafe,
        #ede9fe,
        #fce7f3
    );

    border-radius:30px;
    padding:50px;
    text-align:center;
    border:1px solid #dbe4ff;
    margin-bottom:30px;
}

.hero h1{
    color:#0f172a;
    font-size:48px;
    font-weight:700;
}

.hero p{
    color:#475569;
    font-size:18px;
    margin-top:12px;
}

/* =========================================================
FEATURE CARDS
========================================================= */

.feature-card{
    background:#ffffff;
    border-radius:22px;
    padding:25px;
    text-align:center;
    border:1px solid #dbe4ff;
    box-shadow:0px 4px 12px rgba(99,102,241,0.08);
}

.feature-card h3{
    color:#0f172a;
    font-size:26px;
}

.feature-card p{
    color:#475569;
    font-size:15px;
}

/* =========================================================
DETECTION BOX
========================================================= */

.detect-box{
    background:white;
    padding:24px;
    border-radius:24px;
    border:1px solid #dbe4ff;
    box-shadow:0px 4px 12px rgba(99,102,241,0.08);
}

/* =========================================================
TEXTAREA
========================================================= */

textarea{
    background:#ffffff !important;
    color:#0f172a !important;
    border-radius:16px !important;
    border:1px solid #c7d2fe !important;
    font-size:16px !important;
    caret-color:#7c3aed !important;
}

/* REMOVE RED BORDER */

textarea:focus{
    border:1px solid #8b5cf6 !important;
    box-shadow:0 0 0 1px #8b5cf6 !important;
    outline:none !important;
}

/* PLACEHOLDER */

textarea::placeholder{
    color:#64748b !important;
    opacity:1 !important;
}

/* =========================================================
BUTTON
========================================================= */

.stButton button{
    width:100%;
    height:50px;
    border:none;
    border-radius:14px;

    background:linear-gradient(
        135deg,
        #7c3aed,
        #6366f1
    );

    color:white;
    font-size:17px;
    font-weight:600;
}

/* =========================================================
RESULT BOXES
========================================================= */

.safe-box{
    background:#dcfce7;
    color:#166534;
    padding:22px;
    border-radius:18px;
    font-size:21px;
    font-weight:600;
}

.scam-box{
    background:#fee2e2;
    color:#991b1b;
    padding:22px;
    border-radius:18px;
    font-size:21px;
    font-weight:600;
}

/* =========================================================
AWARENESS BOX
========================================================= */

.awareness{
    background:white;
    border-radius:22px;
    padding:24px;
    border:1px solid #dbe4ff;
    margin-top:20px;
    box-shadow:0px 4px 12px rgba(99,102,241,0.08);
}

.awareness h3{
    color:#7c3aed;
}

.awareness li{
    color:#334155;
    margin-bottom:10px;
    font-size:15px;
}

/* =========================================================
METRIC CARDS
========================================================= */

[data-testid="metric-container"]{
    background:white;
    border-radius:18px;
    padding:18px;
    border:1px solid #dbe4ff;
    box-shadow:0px 4px 12px rgba(99,102,241,0.08);
}

/* METRIC LABEL */

[data-testid="metric-container"] label{
    color:#334155 !important;
    font-size:15px !important;
    font-weight:600 !important;
}

/* METRIC VALUE */

[data-testid="metric-container"] [data-testid="stMetricValue"]{
    color:#0f172a !important;
    font-size:34px !important;
    font-weight:700 !important;
}

/* =========================================================
GRAPH CARDS
========================================================= */

.graph-card{
    background:white;
    padding:12px;
    border-radius:22px;
    border:1px solid #dbe4ff;
    box-shadow:0px 4px 12px rgba(99,102,241,0.08);
    margin-bottom:20px;
}

/* =========================================================
HEADINGS
========================================================= */

h1,h2,h3{
    color:#0f172a !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero">

<h1>🛡️ AI Scam Detection & Awareness System</h1>

<p>
Detect OTP Fraud, Banking Scam, KYC Fraud, Phishing
and Suspicious Messages using Artificial Intelligence
</p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# FEATURE SECTION
# =========================================================

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="feature-card">
    <h3>📩 Smart Detection</h3>
    <p>AI-powered scam and spam detection.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
    <h3>📊 Fraud Analytics</h3>
    <p>Visualize fraud trends and patterns.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
    <h3>🔐 Cyber Awareness</h3>
    <p>Stay protected from cyber scams.</p>
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
    "Enter Your Message",
    height=110,
    placeholder="Paste suspicious SMS, Email or WhatsApp message here..."
)

detect = st.button("Detect Message")

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# DETECTION LOGIC
# =========================================================

if detect:

    cleaned = message.lower()
    cleaned = re.sub(r'[^\w\s]', '', cleaned)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)

    probability = model.predict_proba(vector)

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

        st.markdown("""
        <div class="awareness">

        <h3>⚠️ Scam Awareness Tips</h3>

        <ul>
        <li>Never share OTP, CVV or bank details.</li>
        <li>Do not click suspicious links.</li>
        <li>Verify KYC requests from official apps only.</li>
        <li>Report cyber fraud on helpline 1930.</li>
        <li>Banks never ask for personal details.</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown(f"""
        <div class="safe-box">
        ✅ Safe Message <br><br>
        Confidence Score: {100-scam_prob:.2f}%
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="awareness">

        <h3>🛡️ Cyber Safety Tips</h3>

        <ul>
        <li>Always verify unknown messages.</li>
        <li>Use trusted banking applications.</li>
        <li>Avoid sharing sensitive information online.</li>
        <li>Enable two-factor authentication.</li>
        <li>Stay alert from phishing scams.</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

# =========================================================
# DASHBOARD SECTION
# =========================================================

st.write("")
st.write("")

st.markdown("## 📊 Fraud Analytics Dashboard")

# =========================================================
# METRICS
# =========================================================

m1,m2,m3 = st.columns(3)

with m1:
    st.metric("Total Fraud Cases", len(fraud_data))

with m2:
    st.metric(
        "Most Targeted Area",
        fraud_data['location'].mode()[0]
    )

with m3:
    st.metric(
        "Top Fraud Type",
        fraud_data['fraud_type'].mode()[0]
    )

st.write("")

# =========================================================
# GRAPH 1
# =========================================================

fraud_counts = fraud_data['fraud_type'].value_counts()

fig1 = px.pie(
    values=fraud_counts.values,
    names=fraud_counts.index,
    hole=0.55,
    color_discrete_sequence=[
        "#7c3aed",
        "#6366f1",
        "#8b5cf6",
        "#ec4899",
        "#38bdf8"
    ]
)

fig1.update_layout(
    height=320,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="#111827", size=13),
    title="Fraud Type Distribution",
    title_font=dict(size=20, color="#111827")
)

# =========================================================
# GRAPH 2
# =========================================================

location_counts = fraud_data['location'].value_counts().head(6)

fig2 = px.bar(
    x=location_counts.index,
    y=location_counts.values,
    text=location_counts.values,
    color=location_counts.values,
    color_continuous_scale=[
        "#c4b5fd",
        "#8b5cf6",
        "#6366f1"
    ]
)

fig2.update_layout(
    height=320,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="#111827", size=13),
    title="Most Targeted Locations",
    title_font=dict(size=20, color="#111827"),
    coloraxis_showscale=False
)

# =========================================================
# GRAPH 3
# =========================================================

fig3 = px.histogram(
    fraud_data,
    x="customer_age",
    nbins=15,
    color_discrete_sequence=["#7c3aed"]
)

fig3.update_layout(
    height=320,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="#111827", size=13),
    title="Targeted Age Groups",
    title_font=dict(size=20, color="#111827")
)

# =========================================================
# GRAPH 4
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
    height=320,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="#111827", size=13),
    title="Card Type Fraud Analysis",
    title_font=dict(size=20, color="#111827"),
    coloraxis_showscale=False
)

# =========================================================
# DISPLAY GRAPHS
# =========================================================

g1,g2 = st.columns(2)

with g1:
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with g2:
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

g3,g4 = st.columns(2)

with g3:
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with g4:
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.write("")
st.write("---")

st.markdown("""
<center>

<h4 style='color:#64748b;'>
Developed using Python, Streamlit, Machine Learning,
NLP & Fraud Analytics
</h4>

</center>
""", unsafe_allow_html=True)
