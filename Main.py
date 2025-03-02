import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import cv2
import os

# تحميل الصورة الأصلية
image_path = "WhatsApp Image 2025-02-24 at 19.14.56_af2e2733.jpg"  # تأكد أن الصورة موجودة في نفس مجلد الكود
ndvi_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# التحقق من تحميل الصورة بشكل صحيح
if ndvi_image is None:
    raise FileNotFoundError(f"تعذر تحميل الصورة. تأكد من أن '{image_path}' موجود في نفس مجلد الكود.")

# محاكاة التغير في NDVI بعد 10 سنوات (افتراض زيادة المساحات الخضراء بنسبة 15%)
future_ndvi = np.clip(ndvi_image * 1.15, 0, 255).astype(np.uint8)

# تطبيق K-Means لتصنيف الصورة إلى 3 فئات (خضراء، صحراوية، مختلطة)
flattened = future_ndvi.reshape(-1, 1)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(flattened)
classified_image = labels.reshape(future_ndvi.shape)

# رسم الصورة الأصلية والتوقعية
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# عرض صورة NDVI المستقبلية
axes[0].imshow(future_ndvi, cmap="RdYlGn")
axes[0].set_title("Future NDVI Image")
axes[0].axis("off")

# عرض الصورة المصنفة باستخدام K-Means
axes[1].imshow(classified_image, cmap="viridis")
axes[1].set_title("Future K-Means Classified Image")
axes[1].axis("off")

# تحديد المسار لحفظ الصورة في نفس مجلد الكود
script_dir = os.path.dirname(os.path.abspath(__file__))  # مسار المجلد الذي يحتوي على الكود
future_image_path = os.path.join(script_dir, "future_prediction.png")

# حفظ الصورة
plt.savefig(future_image_path, dpi=300)
plt.show()

print(f"تم حفظ الصورة المتوقعة في: {future_image_path}")
