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

.stApp{
    background-color:#f5f7fb;
}

/* Hide Streamlit menu */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Main spacing */

.block-container{
    padding-top:2rem;
    padding-left:3rem;
    padding-right:3rem;
}

/* Hero */

.hero{
    background:linear-gradient(135deg,#eef2ff,#f5f3ff);
    border-radius:30px;
    padding:50px;
    text-align:center;
    border:1px solid #dbe4ff;
    margin-bottom:30px;
}

.hero h1{
    color:#1e293b;
    font-size:52px;
    font-weight:700;
}

.hero p{
    color:#475569;
    font-size:20px;
}

/* Feature Cards */

.feature-card{
    background:white;
    border-radius:22px;
    padding:25px;
    text-align:center;
    border:1px solid #e2e8f0;
    box-shadow:0px 4px 12px rgba(0,0,0,0.05);
}

.feature-card h3{
    color:#1e293b;
}

.feature-card p{
    color:#64748b;
}

/* Detection Box */

.detect-box{
    background:white;
    padding:25px;
    border-radius:22px;
    border:1px solid #e2e8f0;
    box-shadow:0px 4px 12px rgba(0,0,0,0.05);
}

/* Text Area */

textarea{
    background:#ffffff !important;
    color:#1e293b !important;
    border-radius:16px !important;
    border:2px solid #dbe4ff !important;
    font-size:17px !important;
}

/* Button */

.stButton button{
    width:100%;
    height:52px;
    border:none;
    border-radius:14px;
    background:linear-gradient(135deg,#7c3aed,#6366f1);
    color:white;
    font-size:18px;
    font-weight:600;
}

/* Result Cards */

.safe-box{
    background:#dcfce7;
    color:#166534;
    padding:22px;
    border-radius:18px;
    font-size:22px;
    font-weight:600;
}

.scam-box{
    background:#fee2e2;
    color:#991b1b;
    padding:22px;
    border-radius:18px;
    font-size:22px;
    font-weight:600;
}

/* Awareness Box */

.awareness{
    background:white;
    border-radius:20px;
    padding:25px;
    border:1px solid #e2e8f0;
    margin-top:20px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.05);
}

.awareness h3{
    color:#7c3aed;
}

.awareness li{
    color:#334155;
    margin-bottom:12px;
    font-size:16px;
}

/* Metrics */

[data-testid="metric-container"]{
    background:white;
    border-radius:18px;
    padding:20px;
    border:1px solid #e2e8f0;
    box-shadow:0px 4px 12px rgba(0,0,0,0.05);
}

/* Graph Containers */

.graph-card{
    background:white;
    padding:15px;
    border-radius:20px;
    border:1px solid #e2e8f0;
    box-shadow:0px 4px 12px rgba(0,0,0,0.05);
    margin-bottom:20px;
}

/* Headings */

h1,h2,h3{
    color:#1e293b !important;
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
Protect yourself from OTP Fraud, KYC Scam, Banking Fraud,
Phishing and Online Scam Messages using Artificial Intelligence
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
    <p>AI-powered scam and spam message detection system.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
    <h3>📊 Fraud Analytics</h3>
    <p>Visualize targeted groups and fraud trends.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
    <h3>🔐 Cyber Awareness</h3>
    <p>Spread awareness against phishing and cyber scams.</p>
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
    "",
    height=140,
    placeholder="Paste suspicious SMS, Email or WhatsApp message..."
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

        # Awareness Section

        st.markdown("""
        <div class="awareness">

        <h3>⚠️ Scam Awareness & Prevention Tips</h3>

        <ul>
        <li>Never share OTP, CVV or bank details with anyone.</li>
        <li>Do not click suspicious links received through SMS or WhatsApp.</li>
        <li>Banks never ask for personal information on calls.</li>
        <li>Report cyber fraud immediately on Cyber Helpline 1930.</li>
        <li>Verify KYC requests only from official banking apps.</li>
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

        <h3>🛡️ Stay Safe Online</h3>

        <ul>
        <li>Always verify unknown messages before responding.</li>
        <li>Use official banking and payment applications only.</li>
        <li>Avoid sharing personal information online.</li>
        <li>Enable two-factor authentication for security.</li>
        <li>Stay aware of phishing and fake lottery scams.</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

# =========================================================
# ANALYTICS SECTION
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
        "#60a5fa"
    ]
)

fig1.update_layout(
    height=320,
    paper_bgcolor="white",
    font_color="#1e293b",
    title="Fraud Type Distribution",
    title_font_size=20
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
    color_continuous_scale="purples"
)

fig2.update_layout(
    height=320,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font_color="#1e293b",
    title="Most Targeted Locations",
    title_font_size=20,
    coloraxis_showscale=False
)

# =========================================================
# GRAPH 3
# =========================================================

fig3 = px.histogram(
    fraud_data,
    x="customer_age",
    nbins=15,
    color_discrete_sequence=["#8b5cf6"]
)

fig3.update_layout(
    height=320,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font_color="#1e293b",
    title="Targeted Age Groups",
    title_font_size=20
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
    font_color="#1e293b",
    title="Card Type Fraud Analysis",
    title_font_size=20,
    coloraxis_showscale=False
)

# =========================================================
# GRAPH DISPLAY
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
# PURCHASE CATEGORY GRAPH
# =========================================================

purchase_counts = fraud_data['purchase_category'].value_counts()

fig5 = px.bar(
    x=purchase_counts.index,
    y=purchase_counts.values,
    text=purchase_counts.values,
    color=purchase_counts.values,
    color_continuous_scale="mint"
)

fig5.update_layout(
    height=320,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font_color="#1e293b",
    title="Purchase Category Fraud Analysis",
    title_font_size=20,
    coloraxis_showscale=False
)

st.markdown('<div class="graph-card">', unsafe_allow_html=True)
st.plotly_chart(fig5, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SAFETY AWARENESS SECTION
# =========================================================

st.write("")
st.markdown("## 🔐 Cyber Safety Awareness")

a1,a2,a3 = st.columns(3)

with a1:
    st.markdown("""
    <div class="feature-card">
    <h3>📵 Never Share OTP</h3>
    <p>Bank officials never ask for OTP or PIN.</p>
    </div>
    """, unsafe_allow_html=True)

with a2:
    st.markdown("""
    <div class="feature-card">
    <h3>🔗 Avoid Suspicious Links</h3>
    <p>Do not open unknown or shortened links.</p>
    </div>
    """, unsafe_allow_html=True)

with a3:
    st.markdown("""
    <div class="feature-card">
    <h3>☎️ Report Fraud Quickly</h3>
    <p>Report cyber fraud immediately on helpline 1930.</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.write("")
st.write("---")

st.markdown("""
<center>

<h4 style='color:#64748b;'>
Developed using Python, Streamlit, Machine Learning, NLP & Fraud Analytics
</h4>

</center>
""", unsafe_allow_html=True)
