from django.db import models

# Create your models here

# # -----------------------
# # Sample tour data (mô phỏng)
# # -----------------------
# TOURS = [
#     {"id": "T1", "name": "Hà Nội - Hạ Long 3N2Đ", "price": 3_500_000, "duration": 3, "tags": ["biển", "nghỉ dưỡng", "gia đình"], "rating": 4.5},
#     {"id": "T2", "name": "Đà Nẵng - Hội An 4N3Đ", "price": 5_000_000, "duration": 4, "tags": ["biển", "văn hóa", "ẩm thực"], "rating": 4.7},
#     {"id": "T3", "name": "Sa Pa 3N2Đ", "price": 2_800_000, "duration": 3, "tags": ["núi", "khám phá", "cặp đôi"], "rating": 4.4},
#     {"id": "T4", "name": "Nha Trang 5N4Đ", "price": 6_500_000, "duration": 5, "tags": ["biển", "giải trí", "gia đình"], "rating": 4.6},
#     {"id": "T5", "name": "Phú Quốc 3N2Đ", "price": 4_500_000, "duration": 3, "tags": ["biển", "nghỉ dưỡng", "cao cấp"], "rating": 4.8},
# ]

class Tour(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    duration = models.IntegerField()
    tags = models.CharField(max_length=100)
    rating = models.FloatField()
    thumbnail = models.ImageField(upload_to="tours/", null=True, blank=True)

    def __str__(self):
        return self.name