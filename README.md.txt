

🩺 Smart Disease Diagnosis System | النظام الذكي لتشخيص الأمراض
An End-to-End machine learning system designed to predict potential diseases based on user-input symptoms in Arabic. The system features a 3-tier architecture with a Random Forest model, a Flask API, and a Streamlit frontend.

نظام متكامل يعتمد على تعلم الآلة لتشخيص الأمراض بناءً على الأعراض المدخلة باللغة العربية. يتميز النظام ببنية ثلاثية الطبقات تشمل نموذج Random Forest، واجهة Flask برمجية، وواجهة مستخدم رسومية عبر Streamlit.

🚀 Key Features | المميزات الرئيسية

Multi-Class Classification: Predicts the top 5 most likely diseases.


تصنيف متعدد الفئات: يتنبأ بأكثر 5 أمراض احتمالية.


Probability Calibration: Uses Isotonic Regression to ensure reliable confidence scores.


معايرة الاحتمالات: يستخدم ريغريسيون Isotonic لضمان دقة نسب الثقة.


3-Tier Architecture: Decoupled system with Flask API and Streamlit UI.


بنية ثلاثية الطبقات: نظام منفصل يضم واجهة برمجية (Flask) وواجهة مستخدم (Streamlit).


Full Arabic Support: Symptoms and disease results are fully supported in Arabic.


دعم كامل للغة العربية: الأعراض والنتائج مدعومة باللغة العربية بالكامل.

🛠️ Technical Stack | التقنيات المستخدمة

Model: Random Forest Classifier (Scikit-Learn).


Backend: Flask API.


Frontend: Streamlit UI.


Data Processing: Pandas, NumPy, LabelEncoder.

📂 Project Structure | هيكل المشروع (المحدث)
Plaintext
├── dataset/                  # Dataset folder | مجلد البيانات
├── models/                   # Saved ML models (.pkl) | النماذج المحفوظة
├── app.py                    # Flask API Server | سيرفر الواجهة البرمجية
├── api.py                    # Streamlit Frontend | واجهة المستخدم الرسومية
├── new.ipynb                 # Development Notebook | دفتر تجارب النموذج
├── requirements.txt          # Project dependencies | المكتبات المطلوبة
└── README.md                 # Project documentation | وثيقة المشروع
🚦 How to Run | طريقة التشغيل
Install dependencies | تثبيت المكتبات:

Bash
pip install -r requirements.txt
Run Flask API (The Engine) | تشغيل السيرفر الخلفي:

Bash
python app.py
Run Streamlit UI (The Interface) | تشغيل واجهة المستخدم:

Bash
streamlit run api.py
📊 Performance | الأداء والنتائج
The system achieves improved reliability after applying Probability Calibration, moving confidence scores from skewed low values to realistic statistical probabilities.

حقق النظام موثوقية محسنة بعد تطبيق المعايرة الاحتمالية، حيث تحولت نسب الثقة من قيم منخفضة غير دقيقة إلى احتمالات إحصائية واقعية.

👥 Contributors |
فريق العمل 

Hamza Muyassar / حمزة ميسر 


Assem Mahdi / عاصم مهدي 


Haroon Hatem / هارون حاتم 

Supervised by: Eng. Ayman Al-Tina | تحت إشراف: م. أيمن الطينة