import streamlit as st
import pandas as pd
import requests

# ======================================
# Page Config
# ======================================
st.set_page_config(
    page_title="🩺 النظام الذكي لتشخيص الأمراض",
    page_icon="🧠",
    layout="centered"
)

st.title("🩺 النظام الذكي لتشخيص الأمراض")
st.write("أدخل الأعراض باللغة العربية وسيقوم النظام بتحليلها وتشخيص المرض الأكثر احتمالاً.")

# ======================================
# 🚀 Smart Caching (Data Only)
# ======================================

@st.cache_data
def load_main_data():
    # نحتاج فقط أسماء الأعمدة هنا لغرض العرض، لذا لا يهم إذا تغيرت البيانات قليلاً
    return pd.read_csv("dataset/Final_Augmented_dataset_Diseases_and_Symptoms.csv")

@st.cache_data
def load_translations():
    try:
        df = pd.read_csv("dataset/symptoms_translatedd.csv", on_bad_lines='skip')
        df.columns = df.columns.str.strip()
        df["symptom_en"] = df["symptom_en"].astype(str).str.strip()
        df["symptom_arabic"] = df["symptom_arabic"].astype(str).str.strip()
        return df
    except FileNotFoundError:
        st.error("ملف الترجمة symptoms_translatedd.csv غير موجود.")
        return pd.DataFrame()

@st.cache_data
def load_disease_translation():
    try:
        df = pd.read_csv("dataset/diseaseArabic.csv")
        df["disease_en"] = df["disease_en"].str.strip()
        df["disease_ar"] = df["disease_ar"].str.strip()
        return df
    except FileNotFoundError:
        st.error("ملف ترجمة الأمراض diseaseArabic.csv غير موجود.")
        return pd.DataFrame()

# ======================================
# Load Everything Once
# ======================================
df = load_main_data()
translations_df = load_translations()
disease_df = load_disease_translation()

# ======================================
# Prepare Features
# ======================================
if not df.empty and not translations_df.empty:
    symptoms_en = list(df.columns)
    if "diseases" in symptoms_en:
        symptoms_en.remove("diseases")

    arabic_to_english = dict(zip(
        translations_df["symptom_arabic"],
        translations_df["symptom_en"]
    ))

    symptoms_ar = sorted(list(arabic_to_english.keys()))
    st.write(f"عدد الأعراض المتاحة: {len(symptoms_ar)}")
else:
    symptoms_ar = []
    st.warning("تأكد من وجود ملفات البيانات بشكل صحيح.")

# ======================================
# Symptom Search
# ======================================
search = st.text_input("🔍 ابحث عن عرض:")

filtered_symptoms = [s for s in symptoms_ar if search in s] if search else symptoms_ar

selected_symptoms_ar = st.multiselect(
    "🩺 اختر الأعراض:",
    filtered_symptoms
)

# ======================================
# API Config
# ======================================
# تأكد أن هذا الرابط يطابق عنوان سيرفر Flask
API_URL = "http://127.0.0.1:5000/predict"

# ======================================
# Prediction (TOP 5 via Flask API)
# ======================================
if st.button("🔍 تشخيص المرض"):

    if len(selected_symptoms_ar) == 0:
        st.warning("⚠️ الرجاء اختيار عرض واحد على الأقل.")
    else:
        payload = {
            "symptoms": selected_symptoms_ar   # نرسل القائمة العربية للـ API
        }

        try:
            with st.spinner("🔄 جاري الاتصال بمحرك الذكاء الاصطناعي..."):
                response = requests.post(API_URL, json=payload, timeout=20)

            if response.status_code != 200:
                st.error(f"❌ فشل الاتصال بالخدمة الخلفية. الرمز: {response.status_code}")
                st.stop()

            data = response.json()

        except requests.exceptions.ConnectionError:
            st.error("🚫 تعذر الاتصال بالسيرفر. تأكد أن ملف Flask (app.py) يعمل.")
            st.stop()
        except Exception as e:
            st.error(f"🚫 حدث خطأ غير متوقع: {e}")
            st.stop()

        # ==========================
        # عرض النتائج القادمة من Flask
        # ==========================
        # تحديث النص ليعكس استخدام البايبلاين الجديد
        st.info("🧠 النموذج المستخدم: AI Pipeline (RF + Isotonic Calibration)")

        if "top_predictions" in data:
            results = data["top_predictions"]
            
            if results:
                best_result = results[0]

                st.success(
                    f"🥇 التشخيص الأكثر احتمالاً:\n\n"
                    f"🦠 المرض: **{best_result['disease']}**\n\n"
                    f"📊 نسبة الثقة: **{best_result['confidence']}%**"
                )

                results_df = pd.DataFrame(results)
                st.table(results_df)
            else:
                st.warning("لم يتم العثور على تنبؤات كافية.")
        else:
            st.error("صيغة البيانات القادمة من API غير صحيحة.")

# ======================================
# Footer
# ======================================
st.markdown("---")

