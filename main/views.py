from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

from .models import User, Message, Comment

def show_home_page(request):
    return render(request, "home_page.html")

def show_register_page(request):
    return render(request, "register_page.html")

def show_signin_page(request):
    return render(request, "signin_page.html")

def register_user(request):
    errors = User.objects.basic_validator_register(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect("/register")

    pw_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()


    if len(User.objects.all()) == 0:
        user = User.objects.create(   
            first_name = request.POST["first_name"], 
            last_name = request.POST["last_name"],
            email = request.POST["email"],
            password = pw_hash,
            level = 9
            )
    else:
        user = User.objects.create(   
            first_name = request.POST["first_name"], 
            last_name = request.POST["last_name"],
            email = request.POST["email"],
            password = pw_hash,
            level = 1
            )

    request.session["user_id"] = user.id

    if user.level == 9:
        return redirect("/dashboard/admin")
    else:
        return redirect("/dashboard")

def signin_user(request):
    potential_user = User.objects.filter(email = request.POST["email"])
    if len(potential_user) == 0:
        messages.error(request, "Please check your email and password")
        return redirect("/signin")
    
    user = potential_user[0]

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Please check your email and password")
        return redirect("/signin")
    
    request.session["user_id"] = user.id

    if user.level == 9:
        return redirect("/dashboard/admin")
    else:
        return redirect("/dashboard")

def show_dashboard(request):
    if "user_id" not in request.session:
        messages.error(request, "You are not logged in")
        return redirect("/signin")
    elif "user_id" in request.session and User.objects.get(id = request.session["user_id"]).level == 9:
        return redirect("/dashboard/admin")

    context = {
        'users': User.objects.all(),
        'user': User.objects.get(id = request.session["user_id"])
    }

    return render(request, "dashboard.html", context)

def show_admin_dashboard(request):
    if "user_id" not in request.session:
        messages.error(request, "You are not logged in")
        return redirect("/signin")
    elif "user_id" in request.session and User.objects.get(id = request.session["user_id"]).level != 9:
        messages.error(request, "The page you requested is reserved for admins only")
        return redirect("/dashboard")

    context = {
        'users': User.objects.all(),
        'user': User.objects.get(id = request.session["user_id"])
    }

    return render(request, "admin_dashboard.html", context)

def logout(request):
    request.session.pop("user_id")
    return redirect("/")  

def show_add_user_page(request):
    return render(request, "add_user_page.html")

def add_user(request):
    errors = User.objects.basic_validator_add_user(request.POST)

    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect("/users/new")

    pw_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()

    User.objects.create(   
        first_name = request.POST["first_name"], 
        last_name = request.POST["last_name"],
        email = request.POST["email"],
        password = pw_hash,
        level = request.POST["user_level"]
        )

    return redirect("/dashboard/admin")

def show_user(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
        'messages_posted': Message.objects.filter(recipient = User.objects.get(id=user_id)),
    }
    return render(request, "show_user_page.html", context)

def select_dashboard(request):
    if User.objects.get(id = request.session["user_id"]).level == 9:
        return redirect("/dashboard/admin")
    else:
        return redirect("/dashboard")

def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user
    }

    if request.session["user_id"] == user.id:
        return render(request, "edit_profile.html", context)
    else:
        return render(request, "edit_user.html", context)

def update_user(request, user_id):
    errors = User.objects.basic_validator_edit_user(request.POST, request.session)
 
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect(f"/users/{user_id}/edit")

    user = User.objects.get(id=user_id)
    user.email = request.POST["email"]
    user.first_name = request.POST["first_name"]
    user.last_name = request.POST["last_name"]
    if User.objects.get(id=request.session["user_id"]).level == 9:
        if request.POST["user_level"] == "9":
            user.level = 9
        elif request.POST["user_level"] == "1":
            user.level = 1
    user.save()

    return redirect("/dashboard_selector")

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.session("user_id") == user.id:
        request.session.pop("user_id")
        user.delete()
        return redirect("/")
    
    user.delete()
    return redirect("/dashboard/admin")

def post_message(request, user_id):
    sending_user = User.objects.get(id=request.session["user_id"])
    receiving_user = User.objects.get(id=user_id)
    Message.objects.create(message=request.POST["message"], user = sending_user, recipient = receiving_user)

    return redirect(f"/users/show/{user_id}")

def post_comment(request, user_id):
    sending_user = User.objects.get(id=request.session["user_id"])
    receiving_user = User.objects.get(id=user_id)
    Comment.objects.create(comment=request.POST["comment"], user = sending_user, recipient = receiving_user, message = Message.objects.get(id=request.POST["message_id"])) 

    return redirect(f"/users/show/{user_id}")

def update_password(request, user_id):
    errors = User.objects.basic_validator_update_password(request.POST)

    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect(f"/users/{user_id}/edit")

    user = User.objects.get(id = user_id)
    pw_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
    user.password = pw_hash
    user.save()

    return redirect("/dashboard_selector")













 

