from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Locker
import requests
from django.contrib.auth.decorators import login_required


def rent(request):
    lockerid = request.GET.get("lockerid")

    if not lockerid or not lockerid.isdigit():
        return HttpResponseBadRequest("Некоректный номер шкафчика")

    try:
        lockerid = int(lockerid)
        locker = Locker.objects.get(id=lockerid)
    except Locker.DoesNotExist:
        return HttpResponseNotFound("Шкафчик не найден")

    if locker.isopen:
        return render(request, "rent/lockersrent.html", {
            "id" : locker.id,
            "location": locker.location,
            "size": locker.size,
            "isopen": locker.isopen,
        })
    else:
        return HttpResponseForbidden("Шкафчик занят")

ESP32_IP = 'http://192.168.1.173'
@login_required
def startrental(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Неверный метод запроса")

    lockerid = request.POST.get("lockerid")
    if not lockerid or not lockerid.isdigit():
        return HttpResponseBadRequest("Некорректный номер шкафчика")

    try:
        locker = Locker.objects.get(id=int(lockerid))
    except Locker.DoesNotExist:
        return HttpResponseNotFound("Шкафчик не найден")

    if not locker.isopen:
        return HttpResponseForbidden("Шкафчик занят")

    if Locker.objects.filter(rented_by=request.user).exists():
        return HttpResponseForbidden("У вас уже есть арендованный шкафчик")

    locker.isopen = False
    locker.rented_by = request.user
    locker.save()
    requests.get(f'{ESP32_IP}/locker/startrental')

    return redirect("mylocker")


def mylocker(request):
    locker = Locker.objects.filter(rented_by=request.user).first()
    
    if not locker:
        return render(request, 'rent/mylockers.html', {
            "message": "У вас нет арендованных шкафчиков"
        })

    return render(request, 'rent/mylockers.html', {
        "locker": locker
    })


@login_required
def openlocker(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Неверный метод запроса")

    lockerid = request.POST.get("lockerid")
    if not lockerid or not lockerid.isdigit():
        return HttpResponseBadRequest("Некорректный номер шкафчика")

    try:
        locker = Locker.objects.get(id=int(lockerid), rented_by=request.user)
    except Locker.DoesNotExist:
        return HttpResponseForbidden("Вы не арендовали этот шкафчик")

    requests.get(f'{ESP32_IP}/locker/open')
    return redirect("mylocker")

@login_required
def endrental(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Неверный метод запроса")

    lockerid = request.POST.get("lockerid")
    if not lockerid or not lockerid.isdigit():
        return HttpResponseBadRequest("Некорректный номер шкафчика")

    try:
        locker = Locker.objects.get(id=int(lockerid), rented_by=request.user)
    except Locker.DoesNotExist:
        return HttpResponseForbidden("Вы не арендовали этот шкафчик")

    # Освобождаем шкафчик
    locker.isopen = True
    locker.rented_by = None
    locker.save()

    requests.get(f'{ESP32_IP}/locker/endrental')    

    return redirect("mylocker")