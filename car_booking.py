from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User
 
class Location(models.Model):
    city = models.CharField(max_length=50)
 
    def _str_(self):
        return self.city
 
class CarDealer(models.Model):
    car_dealer = models.OneToOneField(User, on_delete=models.CASCADE)
    phone =  models.CharField(validators = [MinLengthValidator(10), MaxLengthValidator(10)], max_length = 10)
    location = models.OneToOneField(Location, on_delete=models.PROTECT)
    earnings = models.IntegerField(default=0)
    type = models.CharField(max_length=20, blank=True)
 
    def _str_(self):
        return str(self.car_dealer)
 
class Car(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="")
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.PROTECT)
    capacity = models.CharField(max_length=2)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    is_available = models.BooleanField(default=True)
    rent = models.CharField(max_length=10, blank=True)
 
    def _str_(self):
        return self.name
 
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(validators = [MinLengthValidator(10), MaxLengthValidator(10)], max_length = 10)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    type  = models.CharField(max_length=20, blank=True)
 
    def _str_(self):
        return str(self.user)
 
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rent = models.CharField(max_length=10)
    days = models.CharField(max_length=3)
    is_complete = models.BooleanField(default=False)
from django.urls import path
from . import views
 
urlpatterns = [
    path("", views.index, name="index"),
    path("customer_signup/", views.customer_signup, name="customer_signup"),
    path("customer_login/", views.customer_login, name="customer_login"),
    path("car_dealer_signup/", views.car_dealer_signup, name="car_dealer_signup"),
    path("car_dealer_login/", views.car_dealer_login, name="car_dealer_login"),
    path("add_car/", views.add_car, name="add_car"),
    path("all_cars/", views.all_cars, name="all_cars"),
    path("delete_car/<int:myid>/", views.delete_car, name="delete_car"),
    path("customer_homepage/", views.customer_homepage, name="customer_homepage"),
    path("search_results/", views.search_results, name="search_results"),
    path("car_rent/", views.car_rent, name="car_rent"),
    path("order_details/", views.order_details, name="order_details"),
    path("past_orders/", views.past_orders, name="past_orders"),
    path("delete_order/<int:myid>/", views.delete_order, name="delete_order"),
    path("all_orders/", views.all_orders, name="all_orders"),
    path("complete_order/", views.complete_order, name="complete_order"),
    path("earnings/", views.earnings, name="earnings"),
    path("signout/", views.signout, name="signout")
]
<div class="container mt-4">
    <div>
      <h1 class="display-4">ProjectGurukul Online Car Rental System</h1>
      <p class="lead">You can select from the wide range of Cars available.</p>
      <hr class="my-4">
    </div>
    <div class="row mt-4">
{% for car in cars %}
      <div class="col-sm-4 mt-4">
        <div class="card" style="width: 20rem; height: 23rem;">
          <img class="card-img-top" src="/media/{{car.image}}" alt="Card image cap" height="260px">
          <div class="card-body">
            <h5 class="card-title">Car Name: {{car.name}}</h5>
            <h6 class="card-text">Car Dealer: <b>{{car.car_dealer}}</b></h6>
            <p class="card-text">Rent: ₹ {{car.rent}} per day</p>
            <a href="/customer_login/" class="btn btn-primary">Login to Rent </a>
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
def index(request):
    cars = Car.objects.all()
    return render(request, "index.html", {'cars':cars})
<div class="container">
    {% if cars %}
    <h1 class="mt-4">Cars List</h1>
    <div class="users-table mt-4">
        <table>
            <tbody>
                <tr>
                    <th>Car Name</th>
                    <th>Image</th>
                    <th>City</th>
                    <th>Capacity</th>
                    <th>Delete</th>
                </tr>
                {% for car in cars %}
                <tr>
                    <td>{{car.name}}</td>
                    <td><img src="{{car.image.url}}" alt="" width="100px" height="100px"></td>
                    <td>{{car.location.city}}</td>
                    <td>{{car.capacity}}</td>
                    <td><a href="/delete_car/{{car.id}}/" class="btn btn-danger"
                            onclick="return confirm('Are you sure you want to delete {{car.name}}?')">Delete</a></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <br>
        <h2>No Cars Added Yet</h2>
        {% endif %}
    </div>
def all_cars(request):
    dealer = CarDealer.objects.filter(car_dealer=request.user).first()
    cars = Car.objects.filter(car_dealer=dealer)
    return render(request, "all_cars.html", {'cars':cars})
<div class="container">
<form method="POST" enctype="multipart/form-data"> {% csrf_token %}
    <div class="row mt-2">
        <div class="form-group col-md-12">
            <label><i style="font-weight: bold;">Car Name</i></label>
            <input type="text" class="form-control" name="car_name" placeholder="Name of the Car">
        </div>
    </div>
    
    <div class="row mt-3">
        <div class="form-group col-md-6">
            <label><i style="font-weight: bold;">City</i></label>
            <input type="text" class="form-control" name="city" placeholder="City">
        </div>
        <div class="form-group col-md-6">
            <label><i style="font-weight: bold;">Car Image</i></label>
            <input type="file" class="form-control" name="image">
        </div>
    </div>
 
    <div class="row mt-3">
        <div class="form-group col-md-12">
            <label><i style="font-weight: bold;">Capacity</i></label>
            <input type="number" class="form-control" name="capacity" placeholder="Number of Seats">
        </div>
    </div>
 
    <div class="row mt-3">
        <div class="form-group col-md-12">
            <label><i style="font-weight: bold;">Rent</i></label>
            <input type="number" class="form-control" name="rent" placeholder="Rent (per day)">
        </div>
    </div>
 
    <button type="submit" class="btn btn-primary mt-3">Submit</button>
  </form>
  </div>
def add_car(request):
    if request.method == "POST":
        car_name = request.POST['car_name']
        city = request.POST['city']
        image = request.FILES['image']
        capacity = request.POST['capacity']
        rent = request.POST['rent']
        car_dealer = CarDealer.objects.get(car_dealer=request.user)
        try:
            location = Location.objects.get(city=city)
        except:
            location = None
        if location is not None:
            car = Car(name=car_name, car_dealer=car_dealer, location=location, capacity=capacity, image=image, rent=rent)
        else:
            location = Location(city=city)
            car = Car(name=car_name, car_dealer=car_dealer, location=location, capacity=capacity, image=image, rent=rent)
        car.save()
        alert = True
        return render(request, "add_car.html", {'alert':alert})
    return render(request, "add_car.html")
<div class="container mt-5">
    <form method="POST" enctype="multipart/form-data"> {% csrf_token %}
        <div class="row mt-2">
            <div class="form-group col-md-12">
                <label><i style="font-weight: bold;">Car Name</i></label>
                <input type="text" class="form-control" name="car_name" value="{{car.name}}" required>
            </div>
        </div>
        
        <div class="row mt-3">
            <div class="form-group col-md-6">
                <label><i style="font-weight: bold;">City</i></label>
                <input type="text" class="form-control" name="city" value="{{car.location.city}}" required>
            </div>
            <div class="form-group col-md-6">
                <label><i style="font-weight: bold;">Car Image &nbsp;&nbsp;&nbsp;<a href="/media/{{car.image}}/">View Image</a></i></label>
                <input type="file" class="form-control" name="image">
            </div>
        </div>
    
        <div class="row mt-3">
            <div class="form-group col-md-12">
                <label><i style="font-weight: bold;">Capacity</i></label>
                <input type="number" class="form-control" name="capacity" value="{{car.capacity}}" required>
            </div>
        </div>
    
        <div class="row mt-3">
            <div class="form-group col-md-12">
                <label><i style="font-weight: bold;">Rent (per day)</i></label>
                <input type="number" class="form-control" name="rent" value="{{car.rent}}" required>
            </div>
        </div>
    
        <button type="submit" class="btn btn-primary mt-4 btn-lg">Update Details</button>
      </form>
      </div>
def edit_car(request, myid):
    car = Car.objects.filter(id=myid)[0]
    if request.method == "POST":
        car_name = request.POST['car_name']
        city = request.POST['city']
        capacity = request.POST['capacity']
        rent = request.POST['rent']
 
        car.name = car_name
        car.city = city
        car.capacity = capacity
        car.rent = rent
        car.save()
 
        try:
            image = request.FILES['image']
            car.image = image
            car.save()
        except:
            pass
        alert = True
        return render(request, "edit_car.html", {'alert':alert})
    return render(request, "edit_car.html", {'car':car})
<div class="container">
    {% if all_orders %}
    <h1 class="mt-4">Current Orders</h1>
    <div class="users-table mt-4">
        <table>
            <tbody>
                <tr>
                    <th>Customer Name</th>
                    <th>Car Name</th>
                    <th>Image</th>
                    <th>Days</th>
                    <th>Rent</th>
                    <th>Capacity</th>
                    <th>Action</th>
                </tr>
                {% for order in all_orders %}
                <tr>
                    <td>{{order.user.get_full_name}}</td>
                    <td>{{order.car.name}}</td>
                    <td><img src="{{order.car.image.url}}" alt="" width="100px" height="100px"></td>
                    <td>{{order.days}}</td>
                    <td>₹ {{order.rent}}</td>
                    <td>{{order.car.capacity}}</td>
                    <td><form action = "/complete_order/" method="post">
                        {% csrf_token %}
                        <input type="hidden" name="id" value="{{order.id}}">
                        <button class="btn btn-primary " type="submit">Complete</button>
                      </form></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <br>
        <h2>No Orders Right Now</h2>
        {% endif %}
    </div>
def all_orders(request):
    username = request.user
    user = User.objects.get(username=username)
    car_dealer = CarDealer.objects.get(car_dealer=user)
    orders = Order.objects.filter(car_dealer=car_dealer)
    all_orders = []
    for order in orders:
        if order.is_complete == False:
            all_orders.append(order)
    return render(request, "all_orders.html", {'all_orders':all_orders})
<div class="container">
    {% if all_orders %}
    <h1 class="mt-4">Total Earnings: ₹{{amount}}</h1>
    <div class="users-table mt-4">
        <table>
            <tbody>
                <tr>
                    <th>Customer Name</th>
                    <th>Car Name</th>
                    <th>Image</th>
                    <th>Days</th>
                    <th>Rent</th>
                    <th>Capacity</th>
                </tr>
                {% for order in all_orders %}
                <tr>
                    <td>{{order.user.get_full_name}}</td>
                    <td>{{order.car.name}}</td>
                    <td><img src="{{order.car.image.url}}" alt="" width="100px" height="100px"></td>
                    <td>{{order.days}}</td>
                    <td>₹ {{order.rent}}</td>
                    <td>{{order.car.capacity}}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <br>
        <h2>No Earnings Yet</h2>
        {% endif %}
    </div>
def earnings(request):
    username = request.user
    user = User.objects.get(username=username)
    car_dealer = CarDealer.objects.get(car_dealer=user)
    orders = Order.objects.filter(car_dealer=car_dealer)
    all_orders = []
    for order in orders:
        all_orders.append(order)
    return render(request, "earnings.html", {'amount':car_dealer.earnings, 'all_orders':all_orders})
<div class="container ">
  <div class="p-5 bg-light rounded-3">
    <div class="container-fluid">
      <h1 class="display-5 fw-bold">Welcome to ProjectGurukul Online Car Rental System</h1>
      <p class="col-md-8 fs-4">You can enter your city below and see the list of available cars.</p>
    </div>
    <form class="w3-container" action="/search_results/" method="post">
        {% csrf_token %}
        <br><br>
        <label><i style="font-weight: bold; font-size: large;">Enter City Name :</i></label> 
        <input type="text" class="form-control mt-3" name="city"><br>
        <button class="btn btn-primary" type="submit">Search Cars</button>
      </form>
  </div>
</div>
def customer_homepage(request):
    return render(request, "customer_homepage.html")
<div class="container">
    {% if all_orders %}
    <h1 class="mt-4">Past Orders</h1>
    <div class="users-table mt-4">
    <table>
        <tbody>
            <tr>
                <th>Car Name</th>
                <th>Image</th>
                <th>Days</th>
                <th>Rent</th>
                <th>Capacity</th>
                <th>Action</th>
            </tr>
            {% for order in all_orders %}
            <tr>
                <td>{{order.car.name}}</td>
                <td><img src="{{order.car.image.url}}" alt="" width="100px" height="100px"></td>
                <td>{{order.days}}</td>
                <td>₹ {{order.rent}}</td>
                <td>{{order.car.capacity}}</td>
                <td><a href="/delete_order/{{order.id}}/" class="btn btn-danger" onclick="return confirm('Are you sure you want to delete {{car.name}}?')">Delete</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <br>
    <h2>No Past Orders</h2>
    {% endif %}
</div>
def past_orders(request):
    all_orders = []
    user = User.objects.get(username=request.user)
    try:
        orders = Order.objects.filter(user=user)
    except:
        orders = None
    if orders is not None:
        for order in orders:
            if order.is_complete == False:
                order_dictionary = {'id':order.id, 'rent':order.rent, 'car':order.car, 'days':order.days, 'car_dealer':order.car_dealer}
                all_orders.append(order_dictionary)
    return render(request, "past_orders.html", {'all_orders':all_orders})
