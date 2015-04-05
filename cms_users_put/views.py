from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseForbidden

from models import Page


def mostrar(request, resource):
    salida = ""
    if request.user.is_authenticated():
        salida += "<p>Hi " + request.user.username + ". "
        salida += "<a href='/logout/'>Logout</a></p>"
    else:
        salida += "<p>You aren't logged in. "
        salida += "<a href='/admin/login/'>Login!</a></p>"

    if request.method == "GET":
        try:
            fila = Page.objects.get(name=resource)
            return HttpResponse(salida + fila.page)
        except Page.DoesNotExist:
            return HttpResponseNotFound(salida + 'Page not found: ' + resource)
        except Page.MultipleObjectsReturned:
            return HttpResponseNotFound(salida + 'Server allocated more than \
                    one page for that resource')
    elif request.method == "PUT":
        if request.user.is_authenticated():
            newpage = Page(name=resource, page=request.body)
            newpage.save()
            return HttpResponse(salida + "New page added:\n" + request.body)
        else:
            salida += "YOU MUST <a href='/admin/login/'>LOG IN</a>"
            return HttpResponse(salida)
    else:
        return HttpResponseForbidden(salida + "Method not allowed")
