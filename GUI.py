import customtkinter as ctk
import pickle
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import StringVar, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import folium
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os
from PIL import Image
import random
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

import joblib
weather_model = joblib.load("weather_forecast_model.pkl")

data = pd.read_csv("cairo_climate_data.csv")
data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")
root = ctk.CTk()
root.title("Green Vision")
root.geometry("1000x650")

tab_view = ctk.CTkTabview(root)
tab_view.pack(fill="both", expand=True, padx=20, pady=20)

tab_home = tab_view.add("Home")
home_frame = ctk.CTkFrame(tab_home)
home_frame.pack(fill="both", expand=True, padx=20, pady=20)

home_label = ctk.CTkLabel(home_frame, text="Select a region for analysis", font=("Arial", 24, "bold"))
home_label.pack(pady=20)

regions = ["Cairo", "Alexandria", "Giza", "Aswan", "Luxor"]
region_var = StringVar()
region_var.set(regions[0])
region_menu = ctk.CTkComboBox(home_frame, values=regions, variable=region_var)
region_menu.pack(pady=10)

# tab_model1 = tab_view.add("7-Day Prediction")
# model1_frame = ctk.CTkFrame(tab_model1)
# model1_frame.pack(fill="both", expand=True, padx=20, pady=20)

# ctk.CTkLabel(model1_frame, text="Enter past 7 days data:", font=("Arial", 18, "bold")).pack(pady=10)

# entries = []
# for i in range(7):
#     row_frame = ctk.CTkFrame(model1_frame)
#     row_frame.pack(pady=5, padx=10, fill="x")
    
#     ctk.CTkLabel(row_frame, text=f"Day {i+1}", width=80).pack(side="left", padx=5)
#     temp_entry = ctk.CTkEntry(row_frame, placeholder_text="Temperature", width=100)
#     temp_entry.pack(side="left", padx=5)
#     precip_entry = ctk.CTkEntry(row_frame, placeholder_text="Precipitation", width=100)
#     precip_entry.pack(side="left", padx=5)
#     humidity_entry = ctk.CTkEntry(row_frame, placeholder_text="Humidity", width=100)
#     humidity_entry.pack(side="left", padx=5)
    
#     entries.append((temp_entry, precip_entry, humidity_entry))

# result_label = ctk.CTkLabel(model1_frame, text="Results will be displayed here", font=("Arial", 14))
# result_label.pack(pady=10)

# def predict_day8():
#     result_label.configure(text="Prediction: 25°C, 10mm, 60% Humidity")

# predict_button = ctk.CTkButton(model1_frame, text="Predict Day 8", command=predict_day8)
# predict_button.pack(pady=10)

tab_weather = tab_view.add("Weather Forecast")
weather_frame = ctk.CTkFrame(tab_weather)
weather_frame.pack(fill="both", expand=True, padx=20, pady=20)

ctk.CTkLabel(weather_frame, text="Enter the number of years for prediction:", font=("Arial", 18, "bold")).pack(pady=10)
years_entry = ctk.CTkEntry(weather_frame, placeholder_text="Number of years", width=150)
years_entry.pack(pady=5)

text_result = tk.Text(weather_frame, height=10, width=60, state=tk.DISABLED)
text_result.pack(pady=10)

def predict_future():
    try:
        years = int(years_entry.get())
        if years <= 0:
            messagebox.showerror("Error", "Enter a number greater than 0")
            return
        future_dates = pd.date_range(start=data['Date'].max(), periods=years * 365, freq='D')
        future_data = pd.DataFrame({
            'Year': future_dates.year,
            'Month': future_dates.month,
            'Day': future_dates.day
        })
        future_predictions = weather_model.predict(future_data)
        future_data['Temperature (°C)'] = future_predictions[:, 0]
        future_data['Precipitation (mm)'] = future_predictions[:, 1]
        future_data['Humidity (%)'] = future_predictions[:, 2]
        result_text = "📅 Future Predictions:\n" + future_data.head(5).to_string(index=False)
        text_result.config(state=tk.NORMAL)
        text_result.delete(1.0, tk.END)
        text_result.insert(tk.END, result_text)
        text_result.config(state=tk.DISABLED)
        global last_predictions
        last_predictions = future_data
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

def save_to_csv():
    if 'last_predictions' in globals():
        last_predictions.to_csv("future_predictions.csv", index=False)
        messagebox.showinfo("Saved", "Predictions saved to 'future_predictions.csv'")
    else:
        messagebox.showerror("Error", "No predictions made yet!")

predict_button = ctk.CTkButton(weather_frame, text="Predict", command=predict_future)
predict_button.pack(pady=10)

save_button = ctk.CTkButton(weather_frame, text="Save to CSV", command=save_to_csv)
save_button.pack(pady=10)


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
        for widget in ndvi_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()
        
        for i, pred in enumerate(predictions):
            year_frame = ctk.CTkFrame(ndvi_frame)
            year_frame.pack(pady=5, padx=10, fill="x")
            
            ctk.CTkLabel(year_frame, 
                        text=f"Year {i+1}: NDVI = {pred:.4f} - {assess_risk(pred)[0]}", 
                        width=300).pack(side="left", padx=5)
            
            # زر إنشاء تقرير للسنة الحالية
            report_button = ctk.CTkButton(year_frame, 
                                        text="Generate Report", 
                                        command=lambda p=pred, y=i+1: generate_report(p, y))
            report_button.pack(side="right", padx=5)
            
            predicted_ndvi[f"Year {i+1}"] = {"ndvi": pred}
        
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Enter a valid number.")

def assess_risk(ndvi_value):
    if ndvi_value >= 0.5:
        return "✅ Good", "green"
    elif 0.2 <= ndvi_value < 0.5:
        return "⚠ Moderate", "orange"
    else:
        return "🚨 High Risk", "red"

def generate_afforestation_areas(ndvi_value, year):
    base_lat = 30.0444  
    base_lon = 31.2357
    
    areas = []
    num_areas = 5 if ndvi_value < 0.2 else 3 if ndvi_value < 0.4 else 1
    
    for _ in range(num_areas):

        lat = base_lat + random.uniform(-0.05, 0.05)
        lon = base_lon + random.uniform(-0.05, 0.05)
        areas.append({
            "lat": round(lat, 4),
            "lon": round(lon, 4),
            "name": f"Area {_+1} (Year {year})"
        })
    
    return areas

def generate_map(ndvi_value, year):
    map_cairo = folium.Map(location=[30.0444, 31.2357], zoom_start=11)
    
    risk_level, color = assess_risk(ndvi_value)
    areas = generate_afforestation_areas(ndvi_value, year)
    
    for area in areas:
        folium.Marker(
            location=[area["lat"], area["lon"]],
            popup=f"{area['name']}\nRecommended for afforestation",
            icon=folium.Icon(color=color, icon="tree")
        ).add_to(map_cairo)

    map_path = f"map_year_{year}.html"
    map_cairo.save(map_path)
    
    img_data = map_cairo._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img_path = f"map_year_{year}.png"
    img.save(img_path)
    
    return img_path, areas

def generate_report(ndvi_value, year):
    try:
        map_path, areas = generate_map(ndvi_value, year)
        risk_level, _ = assess_risk(ndvi_value)
        solutions = suggest_solutions(ndvi_value)
        
        report_file = f"NDVI_Report_Year_{year}.pdf"
        c = canvas.Canvas(report_file, pagesize=letter)
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, f"🌳 Cairo Afforestation Report - Year {year}")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, f"📊 NDVI Value: {ndvi_value:.4f}")
        c.drawString(100, 710, f"🚩 Risk Level: {risk_level}")
        
        c.drawString(100, 680, "📍 Recommended Afforestation Areas:")
        y_pos = 660
        for area in areas:
            c.drawString(120, y_pos, f"🌐 {area['name']}")
            c.drawString(140, y_pos-20, f"Lat: {area['lat']:.4f}, Lon: {area['lon']:.4f}")
            y_pos -= 40
        
        c.drawString(100, y_pos-40, "💡 Recommended Actions:")
        y_pos -= 60
        for solution in solutions:
            c.drawString(120, y_pos, f"- {solution}")
            y_pos -= 20
        
        c.drawImage(map_path, 100, y_pos-250, width=400, height=300)
        
        c.save()
        messagebox.showinfo("Success", f"✅ Report saved as: {report_file}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate report:\n{e}")

def suggest_solutions(ndvi_value):
    if ndvi_value >= 0.4:
        return [
            "Maintain existing green spaces",
            "Monitor vegetation health"
        ]
    elif 0.2 <= ndvi_value < 0.4:
        return [
            "Plant drought-resistant species",
            "Implement smart irrigation systems",
            "Create urban gardens"
        ]
    else:
        return [
            "Emergency afforestation program",
            "Soil remediation projects",
            "Strict urban planning controls",
            "Community awareness campaigns"
        ]

ctk.CTkButton(ndvi_frame, 
             text="Predict NDVI", 
             command=predict_ndvi,
             fg_color="#2AA876", 
             hover_color="#207A5A").pack(pady=20)


tab_map = tab_view.add("Future City Heatmap")
map_frame = ctk.CTkFrame(tab_map)
map_frame.pack(fill="both", expand=True, padx=20, pady=20)

ctk.CTkLabel(map_frame, text="Cairo now and Cairo in the future after our project", font=("Arial", 18, "bold")).pack(pady=10)

cairo_current_path = "future_NDVI_before.jpg"
cairo_future_path = "future_NDVI_after.png"

current_img_label = ctk.CTkLabel(map_frame)
current_img_label.pack(pady=5)
future_img_label = ctk.CTkLabel(map_frame)
future_img_label.pack(pady=5)

def predict_green_spaces():
    try:
        cairo_current_img = ctk.CTkImage(Image.open(cairo_current_path), size=(400, 300))
        cairo_future_img = ctk.CTkImage(Image.open(cairo_future_path), size=(400, 300))
        
        current_img_label.configure(image=cairo_current_img)
        current_img_label.image = cairo_current_img
        future_img_label.configure(image=cairo_future_img)
        future_img_label.image = cairo_future_img
    
    except Exception as e:
        ctk.CTkLabel(map_frame, text=f"Error loading images: {e}").pack(pady=5)

predict_green_spaces_button = ctk.CTkButton(map_frame, text="Predict Green Spaces", command=predict_green_spaces)
predict_green_spaces_button.pack(pady=10)

guidelines_label = ctk.CTkLabel(map_frame, text="Guidelines for Sustainable Land Use and Agricultural Land Preservation:", font=("Arial", 16, "bold"))
guidelines_label.pack(pady=10)

ctk.CTkLabel(map_frame, text="1. Implement reforestation programs in degraded areas.\n2. Promote water-efficient irrigation techniques.\n3. Encourage urban green spaces and community gardens.\n4. Utilize satellite data for continuous monitoring and early intervention.").pack(pady=5)


root.mainloop()