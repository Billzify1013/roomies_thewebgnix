from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
import base64
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login



# Create your views here.
def index(request):
    hoteldata = Hotel.objects.all()
    return render(request,'index.html',{'hoteldata':hoteldata,})

def hotel_view(request,id):
    if Hotel.objects.filter(id=id).exists():
        hotel = Hotel.objects.get(id=id)
        images = Hotel_all_images.objects.filter(hotel=hotel)[:3]  # Pehli 3 images le rahe hain

        # Alag-alag variables me store karna
        image1 = images[0] if len(images) > 0 else None
        image2 = images[1] if len(images) > 1 else None
        image3 = images[2] if len(images) > 2 else None
        imagecount = Hotel_all_images.objects.filter(hotel=hotel).count()
        hotel_amenities=hotel_aminities.objects.filter(hotel=hotel)
        room_one_category = Room_category.objects.filter(hotel=hotel,is_active=True).first()
        return render(request,'hotel_view.html',{'hotel':hotel,'image1':image1,'image2':image2,'image3':image3,'images':images,
                'imagecount':imagecount,'hotel_amenities':hotel_amenities,'room_one_category':room_one_category})
    else:
        return redirect('index')




def hotel_registration(request):
    return render(request,'hotel_registrationform.html')

def hotel_login(request):
    return render(request,'hotel_login.html')

def newhoteregister(request):
    if request.method == "POST":
        hotel_name = request.POST.get('hotel_name')
        hotel_nearbylandmark = request.POST.get('hotel_nearbylandmark')
        hotel_city = request.POST.get('hotel_city')
        hotel_contact = request.POST.get('hotel_contact')
        hotel_mimage = request.FILES.get('hotel_mimage')
        if Hotel.objects.filter(hotel_contact_number=hotel_contact).exists():
            messages.error(request,'Hotel Number Is Already Registerd! Change The Number For registration')
            return redirect('hotel_registration')
            
        else:
            user, created = User.objects.get_or_create(username=hotel_contact,
                        defaults={'first_name': hotel_name} )

            if created:
                user.set_password(hotel_contact)   # No password required
                user.save()
            else:
                messages.error(request,'Contact Alredy Exists!')
                return redirect('hotel_registration')

            Hotel.objects.create(
                user=user,name=hotel_name,landmark=hotel_nearbylandmark,hotel_city=hotel_city,
                hotel_contact_number=hotel_contact,hotel_main_img=hotel_mimage
            )
       
        messages.success(request,'Hotel Profile Is Created')
        return redirect('hotel_registration')
    else:
        messages.error(request,'Method invalid')
        return redirect('hotel_registration')
    

def hotel_do_login(request):
    if request.method == "POST":
        hotel_contact = request.POST.get('contactnumber')
        password = request.POST.get('password')
        if Hotel.objects.filter(hotel_contact_number=hotel_contact).exists():
            hotel_admin = Hotel.objects.filter(hotel_contact_number=hotel_contact)
            user = authenticate(request, username=hotel_contact,password=password)
            login(request, user)
            return render(request,'hotel_admin.html',{'hotel_admin':hotel_admin})
        else:
            messages.error(request,'Login Denied!')
            return redirect('hotel_login')
        
def Hotel_homepage(request):
    if request.user.is_authenticated:
        user = request.user
        if Hotel.objects.filter(user=user).exists():
            hotel_admin = Hotel.objects.filter(user=user)
            return render(request,'hotel_admin.html',{'hotel_admin':hotel_admin})
        else:
            messages.error(request,'Login Denied!')
            return redirect('hotel_login')


def property_images(request):
    if request.user.is_authenticated :
        user = request.user
        if Hotel.objects.filter(user=user).exists():
            hotel = Hotel.objects.get(user=user)
            img_category = Hotel_image_category.objects.filter(hotel=hotel)
            category_images = {
                category: Hotel_all_images.objects.filter(img_category=category)
                for category in img_category
                }
            return render(request,'hotel_image_page.html',{'img_category':img_category,'category_images':category_images})
        else:
            messages.error(request,'Somthing Went Wrong!')
            return redirect('hotel_login')
        
def create_hotel_img_category(request):
    if request.user.is_authenticated and request.method == "POST":
        user = request.user
        catname = request.POST.get('catname')
        if Hotel.objects.filter(user=user).exists():
            hotel = Hotel.objects.get(user=user)
            if Hotel_image_category.objects.filter(hotel=hotel,image_category_name=catname).exists():
                messages.error(request,'Category Already exists!')
                return redirect('property_images')
            else:
                Hotel_image_category.objects.create(hotel=hotel,image_category_name=catname)
                messages.success(request,'Category Created!')
                return redirect('property_images')
        else:
            messages.error(request,'Somthing Went Wrong!')
            return redirect('hotel_login')
        

def upload_hotel_img(request):
    if request.user.is_authenticated and request.method == "POST":
        user = request.user
        img_category = request.POST.get('img_category')
        image = request.FILES.get('image')
        if Hotel.objects.filter(user=user).exists():
            hotel = Hotel.objects.get(user=user)
            if Hotel_image_category.objects.filter(hotel=hotel,id=img_category).exists():
                category = Hotel_image_category.objects.get(hotel=hotel,id=img_category)
                
                Hotel_all_images.objects.create(hotel=hotel,img_category=category,hotel_img=image)
                messages.success(request,'Image Created!')
                return redirect('property_images')
            else:
                messages.error(request,'Category Not exists!')
                return redirect('property_images')
        else:
            messages.error(request,'Somthing Went Wrong!')
            return redirect('hotel_login')
        
        
def delete_image(request, pk):
    obj = get_object_or_404(Hotel_all_images, pk=pk)
    obj.delete()  # Yeh delete method image file ko bhi delete karega
    messages.success(request,'Image Deleted!')
    return redirect('property_images')


# def showimages(request, id):
#     hoteldata = Hotel_all_images.objects.filter(id=id).first()
#     if hoteldata:
#         allimages = Hotel_all_images.objects.filter(hotel=hoteldata.hotel)
#         hotel_data = Hotel.objects.filter(id=hoteldata.hotel.id)

#         # Unique categories filter karein
#         categories = list(set(image.img_category for image in allimages))

#         return render(request, 'images.html', {
#             'hotel_data': hotel_data,
#             'allimages': allimages,
#             'categories': categories
#         })

def showimages(request, id):
    hoteldata = Hotel_all_images.objects.filter(id=id).first()
    
    if hoteldata:
        hotel = hoteldata.hotel  # Hotel object

        # Room Images ki ek category banayenge
        room_images = room_category_image.objects.filter(hotel=hotel)
        
        # Hotel Categories aur unke images fetch karenge
        hotel_categories = Hotel_image_category.objects.filter(hotel=hotel)
        hotel_category_images = {
            category: Hotel_all_images.objects.filter(img_category=category)
            for category in hotel_categories
        }

        return render(request, 'images.html', {
            'hotel_data': [hotel],  
            'room_images': room_images,  # Room Images ek alag section me dikhenge
            'hotel_categories': hotel_categories,  # Ye categories buttons ke liye
            'hotel_category_images': hotel_category_images  # Category-wise images
        })
    # else:
    #     return HttpResponse("No images found", status=404)



def aminities(request):
    if request.user.is_authenticated :
        user = request.user
        if Hotel.objects.filter(user=user).exists():
            hotel = Hotel.objects.get(user=user)
            hotel_amenities = hotel_aminities.objects.filter(hotel=hotel)
            return render(request,'hotel_amenities_page.html',{'hotel_amenities':hotel_amenities})
        else:
            messages.error(request,'Somthing Went Wrong!')
            return redirect('hotel_login')
        
def save_aminities(request):
    if request.user.is_authenticated and request.method == "POST":
        user = request.user
        icon = request.POST.get('icon')
        servicename = request.POST.get('servicename')
        hotel = Hotel.objects.get(user=user)
        hotel_amenities = hotel_aminities.objects.create(hotel=hotel,
                aminities_name=servicename,icon_code=icon    )
        messages.success(request,'Amenities Created')
        return redirect('aminities')
    
def delete_amenities(request,pk):
    if request.user.is_authenticated :
        user = request.user
        hotel_aminities.objects.filter(id=pk).delete()
        return redirect('aminities')
    else:
        messages.error(request,'Somthing Went Wrong!')
        return redirect('hotel_login')
    

def Rooms_hotel(request):
    if request.user.is_authenticated :
        user = request.user
        if Hotel.objects.filter(user=user).exists():
            hotel = Hotel.objects.get(user=user)
            Category = Room_category.objects.filter(hotel=hotel)
            allimages = room_category_image.objects.filter(hotel=hotel)
            catimages = {}
            for image in allimages:
                if image.category not in catimages:
                    catimages[image.category] = []
                catimages[image.category].append(image)
            return render(request,'hotel_rooms_list.html',{'Category':Category,'catimages':catimages})
        else:
            messages.error(request,'Somthing Went Wrong!')
            return redirect('hotel_login')
    else:
        messages.error(request,'User Not Valid')
        return redirect('hotel_login')
        
def create_rom_category(request):
    if request.user.is_authenticated and request.method == "POST":
        user = request.user
        categoryname = request.POST.get('categoryname')
        categorycode = request.POST.get('categorycode')
        catdescription = request.POST.get('catdescription')
        hotel = Hotel.objects.get(user=user)
        if Room_category.objects.filter(hotel=hotel,category_name=categoryname,category_code=categorycode):
            messages.error(request,'Category Already Exists!')
        else:
            Room_category.objects.create(hotel=hotel,category_name=categoryname,category_code=categorycode,cat_description=catdescription)
            messages.success(request,'Category Created!')

        return redirect('Rooms_hotel')
    else:
        messages.error(request,'User Not Valid')
        return redirect('hotel_login')
     
def save_category_image(request):
    if request.user.is_authenticated and request.method == "POST":
        user = request.user
        img_category = request.POST.get('img_category')
        image = request.FILES.get('image')
        if Room_category.objects.filter(id=img_category).exists() and Hotel.objects.filter(user=user):
            catdata = Room_category.objects.get(id=img_category)
            hotel = Hotel.objects.get(user=user)
            room_category_image.objects.create(hotel=hotel,
                            category=  catdata,hotel_img=image)
            messages.success(request,'Image Created!')
        else:
            messages.error(request,'Category And User Not Found  !')
            return redirect('Rooms_hotel')
        return redirect('Rooms_hotel')
    else:
        messages.error(request,'User Not Valid')
        return redirect('hotel_login')
        

def deletcatimg(request,pk):
    if room_category_image.objects.filter(id=pk).exists():
        room_category_image.objects.filter(id=pk).delete()
        messages.success(request,'Deleted!')
    else:
        messages.error(request,'id not found')
    return redirect('Rooms_hotel')
    

def editcategory(request):
    if request.user.is_authenticated and request.method == "POST":
        user = request.user
        category_id = request.POST.get('category_id')
        category_name = request.POST.get('category_name')
        category_code = request.POST.get('category_code')
        is_active = request.POST.get('is_active')
        cat_description = request.POST.get('cat_description')
        if Room_category.objects.filter(id=category_id).exists():
            Room_category.objects.filter(id=category_id).update(
                category_name=category_name,category_code=category_code,is_active=is_active,cat_description=cat_description
            )
            messages.success(request,'Succesfully Edit!')
        else:
            messages.error(request,'id not found!')
        return redirect('Rooms_hotel')
    else:
        messages.error(request,'User Not Valid')
        return redirect('hotel_login')