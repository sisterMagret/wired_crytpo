
from django.contrib import messages 

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from account.models import User
from account.forms import AddUserForm
from .models import Room



@swagger_auto_schema(
    operation_description="",
    operation_summary="",
)
@require_POST
def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')
    Room.objects.create(uuid=uuid, client=name, url=url)

    return JsonResponse({'message': 'Room created successfully'})





@swagger_auto_schema(
    operation_description="Retrieve product details",
    operation_summary="Retrieve product details",
)
@login_required
def admin(request, *args, **kwargs):
    users = User.objects.filter(is_staff=True)
    rooms =  Room.objects.all()
    return render(request, 'chat/admin.html', {'users': users, 'rooms': rooms})

@login_required
def get_user(request, uuid):
    user = User.objects.get(pk=uuid)
    rooms =  user.rooms.all()
    return render(request, 'chat/user_details.html', {'user': user, 'rooms': rooms})


@login_required
def room(request, uuid):
    room =  Room.objects.filter(uuid=uuid).first()

    if room.status == Room.WAITING:
        room.status = Room.ACTIVE
        room.agent = request.user
        room.save()
    return render(request, 'chat/room.html', {'room': room})


@login_required
def room_delete(request, uuid):
    if request.user.is_superuser:
        room =  Room.objects.filter(uuid=uuid).first()
        room.delete()
        messages.success(request, "Room deleted successfully")
        return redirect('/chat-admin/')
    return redirect('/chat-admin/')
    
    


def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user =  form.save(commit=False)
            user.is_staff = True
            user.set_password(request.POST.get('password'))
            user.save()
            # if user.role == User.MANAGER:
            #     group, created = Group.objects.get_or_create(name='Managers')
            #     if group:
            #         group.user_set.add(user)
            #     else:
            #         group = Group.objects.get(name='Managers')
            #         group.user_set.add(user)
        messages.success(request, "User added")
        return redirect('/chat-admin/')

    else:
            form = AddUserForm()

            return render(request, 'chat/add_user.html', {'form': form})
