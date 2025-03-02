Green-Vision
AI-powered solution to detect desertification, track vegetation loss, and identify optimal afforestation areas using satellite imagery, climate data, and hybrid deep learning models like CNN, LSTM, and U-Net for sustainable land management.

🌍 Desertification Detection and Green Zone Monitoring  

This project aims to detect desertification, track vegetation loss over time, and identify optimal areas for afforestation using advanced AI techniques and satellite data.  

🚀 What We Did:
- Collected satellite imagery from Google Earth Engine, climate data from NOAA, and NDVI vegetation indices.
- Built a hybrid deep learning model combining:
  - CNN for feature extraction from satellite images.
  - LSTM to capture temporal changes over time.
  - XGBoost/Random Forest for structured environmental data.
  - U-Net/SegNet for precise desert area segmentation.
- Generated predictions to highlight:
  - Areas suffering from ongoing desertification.
  - Green zones (parks, trees, agricultural lands).
  - Regions with high potential for reforestation projects.  

🎯 Why It Matters:  
Desertification is a major global challenge, and early detection is key. Our model helps environmental organizations, researchers, and governments make data-driven decisions to combat land degradation and promote sustainability.  

🛠️ Tech Stack:
`Python`, `TensorFlow`, `Keras`, `Google Earth Engine`, `NOAA Data`, `OpenCV`, `Scikit-learn`, `Pandas`, `NumPy`  
