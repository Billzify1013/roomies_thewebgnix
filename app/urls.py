from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index,name="index"),
    path('hotel_view/<int:id>/', views.hotel_view,name="hotel_view"),

    # hotel registration login work here
    path('hotel_registration', views.hotel_registration,name="hotel_registration"),
    path('hotel_login', views.hotel_login,name="hotel_login"),
    path('hotel_do_login', views.hotel_do_login,name="hotel_do_login"),
    path('newhoteregister', views.newhoteregister,name="newhoteregister"),
    path('property_images/', views.property_images, name='property_images'),
    path('create_hotel_img_category/', views.create_hotel_img_category, name='create_hotel_img_category'),
    path('upload_hotel_img/', views.upload_hotel_img, name='upload_hotel_img'),
    path('delete-image/<int:pk>/', views.delete_image, name='delete-image'),
    path('delete_amenities/<int:pk>/', views.delete_amenities, name='delete_amenities'),
    path('showimages/<int:id>/', views.showimages, name='showimages'),
    path('aminities/', views.aminities, name='aminities'),
    path('save_aminities/', views.save_aminities, name='save_aminities'),
    path('Rooms_hotel/', views.Rooms_hotel, name='Rooms_hotel'),
    path('create_rom_category/', views.create_rom_category, name='create_rom_category'),
    path('save_category_image/', views.save_category_image, name='save_category_image'),
    path('deletcatimg/<int:pk>/', views.deletcatimg, name='deletcatimg'),
    path('editcategory/', views.editcategory, name='editcategory'),
    path('Hotel_homepage/', views.Hotel_homepage, name='Hotel_homepage'),

    


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
