from django.db import models

# Create your models here.
# class VaccineType:
#     """
#     WigetType
#     - simpleWidget, LayoutWidget
#     """
#     SIMPLE_VACCINE_D = 'simple_widget_d'
#     SIMPLE_VACCINE_A = 'simple_widget_a'
#     SIMPLE_VACCINE_G = 'simple_widget_g'

#     ALL_VACCINE = 'all_vaccine'

#     VACCINE_TYPES = [
#         (SIMPLE_VACCINE_D, '대상포진'),
#         (SIMPLE_VACCINE_A, 'A형 간염'),
#         (SIMPLE_VACCINE_G, '가다실'),
#     ]


# class StoreWidget(models.Model):
#     # download = models.IntegerField(default=0)
#     vaccine_type = models.CharField(
#         max_length=31, 
#         choices=VaccineType.VACCINE_TYPES,
#         default=VaccineType.ALL_VACCINE,
#         help_text= '백신 종류'
#     )
#     description = models.CharField(max_length=255, null=True, blank=True, help_text="병원설명")
#     name = models.CharField(max_length=63, null=True, blank=True, help_text='병원이름')
#     # is_removed = models.BooleanField(default=False)
#     # score = models.IntegerField(default=0)
#     # image=models.ImageField(upload_to="storewidgets/", blank=True, null=True)



# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)#병원명
    # 최대길이가 200자라는 말
    # writer=models.CharField(max_length=100,null=True)#백신명
    detail=models.CharField(max_length=100,null=True)#백신명
    # pub_date=models.DateTimeField()
    body=models.TextField()#병원정보/주소
    maxprice=models.CharField(max_length=100, null=True)#최고가격
    minprice=models.CharField(max_length=100, null=True)#최저가격

    image=models.ImageField(upload_to='image', blank=True, null=True)

    def __str__(self):
        return self.title