# import customtkinter as ctk
# import pickle
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from tkinter import StringVar
# import folium
# from tkintermapview import TkinterMapView
# from io import BytesIO
# from PIL import Image, ImageTk

# # Load Models
# with open("mymodel1.pkl", "rb") as file:
#     model1 = pickle.load(file)

# with open("my_model_years.pkl", "rb") as file:
#     model_years_model = pickle.load(file)

# with open("ndvi_kmeans_model.pkl", "rb") as file:
#     heatmap_model = pickle.load(file)

# # Initialize main window
# ctk.set_appearance_mode("Dark")
# ctk.set_default_color_theme("green")
# root = ctk.CTk()
# root.title("Desertification Prediction App")
# root.geometry("1000x650")

# # Create Tab View
# tab_view = ctk.CTkTabview(root)
# tab_view.pack(fill="both", expand=True, padx=20, pady=20)

# # Home Page
# tab_home = tab_view.add("Home")
# home_frame = ctk.CTkFrame(tab_home)
# home_frame.pack(fill="both", expand=True, padx=20, pady=20)

# home_label = ctk.CTkLabel(home_frame, text="Select a region for analysis", font=("Arial", 24, "bold"))
# home_label.pack(pady=20)

# regions = ["Cairo", "Alexandria", "Giza", "Aswan", "Luxor"]
# region_var = StringVar()
# region_var.set(regions[0])

# region_menu = ctk.CTkComboBox(home_frame, values=regions, variable=region_var)
# region_menu.pack(pady=10)

# # Final Page - NDVI and K-Means Classification with Map
# tab_map = tab_view.add("Future City Heatmap")
# map_frame = ctk.CTkFrame(tab_map)
# map_frame.pack(fill="both", expand=True, padx=20, pady=20)

# ctk.CTkLabel(map_frame, text="Land Classification Map", font=("Arial", 18, "bold")).pack()

# map_label = ctk.CTkLabel(map_frame)
# map_label.pack()

# def update_map():
#     selected_region = region_var.get()
#     locations = {
#         "Cairo": [30.0444, 31.2357],
#         "Alexandria": [31.2001, 29.9187],
#         "Giza": [30.0131, 31.2089],
#         "Aswan": [24.0889, 32.8998],
#         "Luxor": [25.6872, 32.6396]
#     }
#     lat, lon = locations[selected_region]
    
#     m = folium.Map(location=[lat, lon], zoom_start=10)
    
#     # Add land classification markers
#     folium.Marker([lat + 0.05, lon], tooltip="Suitable for Agriculture", icon=folium.Icon(color='yellow')).add_to(m)
#     folium.Marker([lat - 0.05, lon], tooltip="Unsuitable for Agriculture", icon=folium.Icon(color='red')).add_to(m)
#     folium.Marker([lat, lon + 0.05], tooltip="Already Cultivated", icon=folium.Icon(color='green')).add_to(m)
    
#     # Save map as an image
#     img_data = BytesIO()
#     m.save("map.html")
    
#     import imgkit
#     imgkit.from_file("map.html", "map.png")
#     img = Image.open("map.png")
#     img = img.resize((800, 500))
#     map_img = ImageTk.PhotoImage(img)
#     map_label.configure(image=map_img)
#     map_label.image = map_img
    
# show_map_button = ctk.CTkButton(map_frame, text="Generate Map", command=update_map)
# show_map_button.pack(pady=10)

# # Run main loop
# root.mainloop()
















# import tkinter as tk
# from tkinter import messagebox
# import pandas as pd
# import numpy as np
# import joblib

# # 🔹 تحميل النموذج
# from joblib import load
# import tkinter.messagebox as messagebox  # للتعامل مع رسائل الخطأ

# try:
#     model = load("weather_forecast_model.pkl")  # تأكد أن الملف موجود في نفس المجلد
#     print("✅ تم تحميل النموذج بنجاح:", type(model))
# except Exception as e:
#     messagebox.showerror("خطأ", f"فشل تحميل النموذج:\n{e}")
#     exit()



# # 🔹 تحميل البيانات الأصلية لاستخراج آخر تاريخ متاح
# data = pd.read_csv("cairo_climate_data.csv")
# data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')

# def predict_future():
#     """تنفيذ التنبؤات لعدد معين من السنوات وعرض النتائج في الواجهة."""
#     try:
#         years = int(entry_years.get())  # الحصول على عدد السنوات المدخلة
#         if years <= 0:
#             messagebox.showerror("خطأ", "يجب إدخال عدد سنوات أكبر من 0")
#             return
        
#         # 🔹 إنشاء تواريخ المستقبل بناءً على آخر تاريخ متاح
#         future_dates = pd.date_range(start=data['Date'].max(), periods=years*365, freq='D')
#         future_data = pd.DataFrame({
#             'Year': future_dates.year,
#             'Month': future_dates.month,
#             'Day': future_dates.day
#         })
        
#         # 🔹 تنفيذ التنبؤات باستخدام النموذج المحمل
#         future_predictions = model.predict(future_data)
        
#         # 🔹 إعداد النتائج
#         future_data['Predicted Temperature (°C)'] = future_predictions[:, 0]
#         future_data['Predicted Precipitation (mm)'] = future_predictions[:, 1]
#         future_data['Predicted Humidity (%)'] = future_predictions[:, 2]
        
#         # 🔹 عرض أول 5 توقعات فقط
#         result_text = "📅 التوقعات المستقبلية:\n"
#         result_text += future_data.head(5).to_string(index=False)
        
#         # تحديث مربع النتائج
#         text_result.config(state=tk.NORMAL)
#         text_result.delete(1.0, tk.END)
#         text_result.insert(tk.END, result_text)
#         text_result.config(state=tk.DISABLED)

#         # حفظ النتائج في متغير للاستخدام في زر الحفظ
#         global last_predictions
#         last_predictions = future_data

#     except ValueError:
#         messagebox.showerror("خطأ", "يرجى إدخال رقم صحيح!")

# def save_to_csv():
#     """حفظ التوقعات الأخيرة في ملف CSV."""
#     if 'last_predictions' in globals():
#         last_predictions.to_csv("future_predictions.csv", index=False)
#         messagebox.showinfo("تم الحفظ ✅", "تم حفظ التوقعات في ملف 'future_predictions.csv'")
#     else:
#         messagebox.showerror("خطأ", "لم يتم تنفيذ أي توقعات بعد!")

# # 🔹 إنشاء نافذة GUI
# root = tk.Tk()
# root.title("🔮 توقعات الطقس المستقبلية")
# root.geometry("500x450")
# root.resizable(False, False)

# # 🔹 العنوان
# label_title = tk.Label(root, text="🔮 توقعات الطقس المستقبلية", font=("Arial", 14, "bold"))
# label_title.pack(pady=10)

# # 🔹 إدخال عدد السنوات
# label_years = tk.Label(root, text="أدخل عدد السنوات للتنبؤ:")
# label_years.pack()
# entry_years = tk.Entry(root, width=10)
# entry_years.pack(pady=5)

# # 🔹 زر تنفيذ التنبؤ
# btn_predict = tk.Button(root, text="🔍 تنبؤ", command=predict_future, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
# btn_predict.pack(pady=10)

# # 🔹 مربع نص لعرض النتائج
# text_result = tk.Text(root, height=10, width=50, state=tk.DISABLED)
# text_result.pack(pady=10)

# # 🔹 زر حفظ النتائج إلى CSV
# btn_save = tk.Button(root, text="💾 حفظ إلى CSV", command=save_to_csv, bg="#008CBA", fg="white", font=("Arial", 12, "bold"))
# btn_save.pack(pady=10)

# # تشغيل الواجهة
# root.mainloop()
import customtkinter as ctk
import pickle
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import StringVar, messagebox
import folium
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from PIL import Image

# تحميل النماذج
try:
    with open("mymodel1.pkl", "rb") as file:
        model1 = pickle.load(file)
    with open("weather_forecast_model.pkl", "rb") as file:
        weather_model = pickle.load(file)
    with open("ndvi__model.pkl", "rb") as file:
        ndvi_model = pickle.load(file)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load model:\n{e}")
    exit()

# إعداد واجهة المستخدم
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")
root = ctk.CTk()
root.title("Green Vision")
root.geometry("1000x650")

tab_view = ctk.CTkTabview(root)
tab_view.pack(fill="both", expand=True, padx=20, pady=20)

# تبويب التنبؤ بـ NDVI
tab_ndvi = tab_view.add("NDVI Prediction")
ndvi_frame = ctk.CTkFrame(tab_ndvi)
ndvi_frame.pack(fill="both", expand=True, padx=20, pady=20)

ctk.CTkLabel(ndvi_frame, text="Enter number of years for NDVI prediction:", font=("Arial", 18, "bold")).pack(pady=10)
years_entry_ndvi = ctk.CTkEntry(ndvi_frame, placeholder_text="Years", width=150)
years_entry_ndvi.pack(pady=5)

# وظيفة للتنبؤ بـ NDVI
def predict_ndvi():
    try:
        years = int(years_entry_ndvi.get())
        future_steps = years
        initial_input = np.array([[0.04], [0.04], [0.05], [0.1], [0.1]])
        initial_input = initial_input.reshape(1, 5, 1)
        predictions = []
        for _ in range(future_steps):
            next_prediction = ndvi_model.predict(initial_input)[0, 0]
            predictions.append(next_prediction)
            initial_input = np.append(initial_input[:, 1:, :], [[[next_prediction]]], axis=1)
            initial_input = initial_input.reshape(1, 5, 1)
        
        # عرض التنبؤات لكل سنة
        global predicted_ndvi
        predicted_ndvi = {}
        for i, pred in enumerate(predictions):
            year_frame = ctk.CTkFrame(ndvi_frame)
            year_frame.pack(pady=5, padx=10, fill="x")
            
            ctk.CTkLabel(year_frame, text=f"Year {i+1}: NDVI = {pred:.4f}", width=200).pack(side="left", padx=5)
            
            # زر إنشاء تقرير للسنة الحالية
            report_button = ctk.CTkButton(year_frame, text="Generate Report", command=lambda p=pred, y=i+1: generate_report(p, y))
            report_button.pack(side="right", padx=5)
            
            predicted_ndvi[f"Year {i+1}"] = {"lat": 30.0444, "lon": 31.2357, "ndvi": pred}
        
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Enter a valid number.")

ndvi_button = ctk.CTkButton(ndvi_frame, text="Predict NDVI", command=predict_ndvi)
ndvi_button.pack(pady=10)

# وظيفة لتقييم المخاطر بناءً على NDVI
def assess_risk(ndvi_value):
    if ndvi_value >= 0.4:
        return "✅ Good", "No immediate environmental concerns."
    elif 0.2 <= ndvi_value < 0.4:
        return "⚠ Moderate", "Vegetation is declining. Intervention needed."
    else:
        return "🚨 High Risk", "Severe vegetation loss. Urgent action required."

# وظيفة لاقتراح الحلول
def suggest_solutions(ndvi_value):
    if ndvi_value >= 0.4:
        return ["✅ Maintain current green spaces."]
    elif 0.2 <= ndvi_value < 0.4:
        return [
            "🌿 Increase tree planting in urban areas.",
            "🏡 Establish more public parks.",
            "💧 Improve irrigation and water supply."
        ]
    else:
        return [
            "🌲 Large-scale afforestation required.",
            "🏗 Limit urban expansion in critical areas.",
            "🌍 Reduce pollution and improve air quality.",
            "🚰 Enhance water management for vegetation support."
        ]

# وظيفة لإنشاء الخريطة
def generate_map(ndvi_value):
    map_cairo = folium.Map(location=[30.0444, 31.2357], zoom_start=11)
    
    # تحديد لون الماركر بناءً على قيمة NDVI
    if ndvi_value >= 0.4:
        color = "green"
    elif 0.2 <= ndvi_value < 0.4:
        color = "orange"
    else:
        color = "red"
    
    folium.Marker(
        location=[30.0444, 31.2357],
        popup=f"Cairo NDVI: {ndvi_value:.2f}",
        icon=folium.Icon(color=color, icon="tree")
    ).add_to(map_cairo)

    map_cairo.save("cairo_tree_map.html")

    # تحويل الخريطة إلى صورة
    img_data = map_cairo._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img_path = "map.png"
    img.save(img_path)

    return img_path

# وظيفة لإنشاء تقرير PDF
def generate_report(ndvi_value, year):
    report_file = f"NDVI_Report_Year_{year}.pdf"
    c = canvas.Canvas(report_file, pagesize=letter)

    # عنوان التقرير
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, f"📋 NDVI Environmental Report - Year {year}")

    c.setFont("Helvetica", 12)
    y = 730

    # عرض نتائج NDVI
    risk_level, warning = assess_risk(ndvi_value)
    solutions = suggest_solutions(ndvi_value)

    c.drawString(100, y, f"📌 Cairo: NDVI = {ndvi_value:.2f}")
    c.drawString(120, y - 20, f"🔹 Risk Level: {risk_level}")
    c.drawString(120, y - 40, f"⚠ Warning: {warning}")

    # الحلول المقترحة
    y -= 60
    c.drawString(120, y, "💡 Recommended Solutions:")
    y -= 20
    for solution in solutions:
        c.drawString(140, y, f"- {solution}")
        y -= 20

    y -= 20  # مساحة إضافية

    # إضافة الخريطة
    c.drawString(100, y - 20, "🗺 NDVI Map for Cairo:")
    map_path = generate_map(ndvi_value)
    y -= 180
    c.drawImage(map_path, 100, y, width=400, height=250)

    c.save()
    messagebox.showinfo("Success", f"✅ Report generated successfully: {report_file}")

root.mainloop()