from .models import category_master, Cart


def cat_pro_list(request):
    datas = category_master.objects.all()
    return {"nav_pro_cat": datas}


def car_count(request):
    if request.user.is_authenticated:
        cart_l = len(Cart.objects.filter(user=request.user))
    else:
        cart_l = 0
    return {'cart_len': cart_l}