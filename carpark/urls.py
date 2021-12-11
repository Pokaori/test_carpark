"""carpark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from driver.views import DriverViewSet
from vehicle.views import VehicleViewSet, VehicleSetDriverViewSet

router_driver = routers.DefaultRouter()
router_driver.register('driver', DriverViewSet)

router_vehicle = routers.DefaultRouter()
router_vehicle.register('vehicle', VehicleViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('drivers/', include(router_driver.urls)),
    path('vehicles/', include(router_vehicle.urls)),
    path('vehicles/set_driver/<int:pk>', VehicleSetDriverViewSet.as_view({'post': 'set_driver'}), name="set-driver"),
]
