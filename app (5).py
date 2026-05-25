
import streamlit as st
import pandas as pd
import pickle
import re

# LOAD TRAINED MODEL

model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# LOAD FRAUD ANALYTICS DATASET
fraud_data = pd.read_csv("Inclusive_Indian_Fraud_Dataset.csv")


# PAGE SETTINGS

st.set_page_config(
    page_title="AI Scam Detection System",
    page_icon="🛡️",
    layout="wide"
)

# TITLE

st.title("🛡️ AI Scam Detection & Fraud Analytics System")

st.write(
    "Detect Scam, Spam, OTP Fraud, KYC Fraud, Phishing Messages "
    "and View Real-Time Fraud Analytics"
)

# SIDEBAR

st.sidebar.title("Navigation")

option = st.sidebar.radio(
    "Go To",
    [
        "Scam Detection",
        "Fraud Analytics Dashboard"
    ]
)

# SCAM DETECTION SECTION

if option == "Scam Detection":

    st.header("📩 Scam Message Detection")

    message = st.text_area(
        "Enter Message Here"
    )

    if st.button("Detect Message"):

        # Check empty input
        if message.strip() == "":
            st.warning("⚠️ Please enter a message")
        else:

          
            # TEXT PREPROCESSING

            msg = message.lower()

            msg = re.sub(r'[^\w\s]', '', msg)

            # =========================
            # TEXT VECTORIZATION
            # =========================

            data = vectorizer.transform([msg])

            # =========================
            # PREDICTION
            # =========================

            prediction = model.predict(data)

            probability = model.predict_proba(data)

            scam_prob = probability[0][1] * 100

            # =========================
            # RESULT
            # =========================

            st.subheader("Result")

            if prediction[0] == 1:

                st.error(
                    f"🚨 Scam / Spam Message Detected\n\n"
                    f"Confidence: {scam_prob:.2f}%"
                )

            else:

                st.success(
                    f"✅ Safe Message\n\n"
                    f"Confidence: {100 - scam_prob:.2f}%"
                )

            # =========================
            # KEYWORD ANALYSIS
            # =========================

            scam_keywords = [
                "otp",
                "kyc",
                "lottery",
                "winner",
                "click",
                "bank",
                "account",
                "verify",
                "urgent",
                "prize",
                "money",
                "offer",
                "loan",
                "free",
                "gift"
            ]

            found_keywords = []

            for word in scam_keywords:
                if word in msg:
                    found_keywords.append(word)

            st.subheader("Detected Suspicious Keywords")

            if len(found_keywords) > 0:
                st.write(found_keywords)
            else:
                st.write("No suspicious keywords found")

# =========================================================
# FRAUD ANALYTICS DASHBOARD
# =========================================================

elif option == "Fraud Analytics Dashboard":

    st.header("📊 Fraud Analytics Dashboard")

    # =========================
    # SHOW DATASET
    # =========================

    st.subheader("Dataset Preview")

    st.dataframe(fraud_data.head())

    # =========================
    # TOTAL CASES
    # =========================

    st.subheader("📌 Total Fraud Cases")

    st.metric(
        label="Total Cases",
        value=len(fraud_data)
    )

    # =========================
    # AGE GROUP ANALYSIS
    # =========================

    if 'Age' in fraud_data.columns:

        st.subheader("👥 Fraud Cases by Age")

        age_counts = fraud_data['Age'].value_counts()

        st.bar_chart(age_counts)

    # =========================
    # STATE WISE FRAUD
    # =========================

    if 'State' in fraud_data.columns:

        st.subheader("📍 State Wise Fraud Cases")

        state_counts = fraud_data['State'].value_counts()

        st.bar_chart(state_counts)

    # =========================
    # FRAUD TYPE ANALYSIS
    # =========================

    if 'Fraud_Type' in fraud_data.columns:

        st.subheader("🚨 Fraud Type Distribution")

        fraud_counts = fraud_data['Fraud_Type'].value_counts()

        st.bar_chart(fraud_counts)

    # =========================
    # GENDER ANALYSIS
    # =========================

    if 'Gender' in fraud_data.columns:

        st.subheader("⚧ Gender Wise Fraud Cases")

        gender_counts = fraud_data['Gender'].value_counts()

        st.bar_chart(gender_counts)

    # =========================
    # STATE FILTER
    # =========================

    if 'State' in fraud_data.columns:

        st.subheader("🔍 Filter Data by State")

        selected_state = st.selectbox(
            "Select State",
            fraud_data['State'].unique()
        )

        filtered_data = fraud_data[
            fraud_data['State'] == selected_state
        ]

        st.write(filtered_data)

# =========================
# FOOTER
# =========================

st.write("---")

st.write(
    "Developed using Python, Streamlit, NLP, Machine Learning & Fraud Analytics"
)
