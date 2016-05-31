from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# import json
# import datetime
#
# from django.db.models import Q
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.core.mail import send_mail
# Create your views here.

def login(request):
    return render(request, 'login.html')


    # send_mail('Pedido de Cliente', mess_pedido,
    #               'postmaster@sandbox3cb2aeaee26e40d99701d79339faccce.mailgun.org',
    #               ['sac.dcher@gmail.com', 'caiodotdev@gmail.com'], fail_silently=False)

    # def get_data_formated(data):
    #     # replace = data.replace('/', '-')
    #     date = datetime.datetime.strptime(data, '%d/%m/%Y')
    #     new_d = datetime.datetime.strftime(date, '%Y-%m-%d')
    #     return new_d
