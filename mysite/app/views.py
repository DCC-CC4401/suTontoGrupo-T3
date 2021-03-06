# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import LoginForm
from .forms import EditVForm
from .forms import SignupForm
from .forms import ProductForm
from .models import *
from django.contrib import auth


def index(request):
    user = User.objects.filter(is_active=1)
    return render(request, 'app/index.html', {'user': user})


def logout(request):
    user = User.objects.get(is_active=1)
    user.is_active = 0
    user.save()
    return index(request)


def login(request):
    form = LoginForm(request.POST)
    # formulario lleno, edicion de datos
    if request.method == 'POST' and form.is_valid():
        # obtengo mail y pass
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # veo si estan en la bd
        try:
            user = User.objects.get(username=username)
            if UserInfo.objects.get(user=user) != None:
                if user.password == password:
                    user.is_active = 1
                    user.save()
                    usuario = UserInfo.objects.get(user=user)
                    if usuario.tipo == 'fijo':
                        usuario = VendedorFijo.objects.get(user=user)
                        return render(request, 'app/vendedor_profile.html',
                                      {'menus': get_menus(user.username), 'usuario': usuario, 'user': user})
                    elif usuario.tipo == "ambulante":
                        usuario = VendedorAmbulante.objects.get(user=user)
                        return render(request, 'app/vendedor_profile.html',
                                      {'menus': get_menus(user.username), 'usuario': usuario, 'user': user})
                    else:  # es alumno
                        return render(request, 'app/index.html', {'usuario': usuario, 'user': user})
                else:
                    return render(request, 'app/login2.html', {'form': form})
        except Exception:
            return render(request, 'app/login2.html', {'form': form})
    else:
        return render(request, 'app/login.html', {'form': form})


def gestion_productos(request):
    user = User.objects.filter(is_active=1)
    return render(request, 'app/gestion_productos.html', {'user': user})


def home(request):
    user = User.objects.filter(is_active=1)
    return render(request, 'app/home.html', {'user': user})


def signup(request):
    page = "app/signup.html"
    clienteNul = User(username="nulo")
    cliente = UserInfo(user=clienteNul)
    # recibe el form
    if (request.method == 'POST'):
        print("1")
        form = SignupForm(request.POST)
        print(request.POST)
        print(form.errors)
        if (form.is_valid()):

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usertype = form.cleaned_data['usertype']
            email = form.cleaned_data['email']
            hora_inicial = form.cleaned_data['hora_inicial']
            hora_final = form.cleaned_data['hora_final']
            efectivo = form.cleaned_data['efectivo']
            tarjeta_credito = form.cleaned_data['tarjeta_credito']
            tarjeta_debito = form.cleaned_data['tarjeta_debito']
            tarjeta_junaeb = form.cleaned_data['tarjeta_junaeb']
            if (int(usertype[0]) == 3):  # es un cliente
                print("entre!!")
                user = User(username=username, email=email, password=password)
                user.is_active = 1
                user.save()
                cliente = Alumno(user=User.objects.get(username=username), tipo='alumno')
                cliente.save()
                page = 'app/index.html'
                return render(request, 'app/index.html')

            elif (int(usertype[0]) == 1):  # es un vendedor fijo

                user = User(username=username, email=email, password=password)
                user.is_active = 1
                user.save()
                cliente = VendedorFijo(user=User.objects.get(username=username), tipo='fijo',
                                       nombre_visible=username,
                                       apertura=hora_inicial, cierre=hora_final,
                                       tarj_cred=(True if (tarjeta_credito == 'on') else False),
                                       tarj_deb=(True if (tarjeta_debito == 'on') else False),
                                       tarj_junaeb=(True if (tarjeta_junaeb == 'on') else False))
                cliente.save()
                return vendedor_profile(request)
            elif (int(usertype[0]) == 2):  # es un vendedor ambulante

                user = User(username=username, email=email, password=password)
                user.is_active = 1
                user.save()
                cliente = VendedorAmbulante(user=User.objects.get(username=username), tipo='ambulante',
                                            tarj_cred=(True if (tarjeta_credito == 'on') else False),
                                            tarj_deb=(True if (tarjeta_debito == 'on') else False),
                                            tarj_junaeb=(True if (tarjeta_junaeb == 'on') else False))
                cliente.save()
                page = 'app/vendedor_profile.html'
                return vendedor_profile(request)

    form = SignupForm()
    return render(request, 'app/signup.html', {'form': form})


def get_info(producto):
    info = {
        'nombre': producto.nombre,
        'user': producto.user,
        'precio': producto.precio,
        'decripcion': producto.descripcion,
        'categoria': producto.categoria,
        'stock': producto.stock,
        'icono': producto.imagen,
        'imagen': producto.img_referencia,
    }
    return info


def get_menus(user):
    productos = []
    for i in Productos.objects.filter(user=user):
        productos.append(get_info(i))
    return productos


def vendedor_profile(request):
    usuario = User.objects.get(is_active=1)
    user = User.objects.get(username=usuario.username)
    info_producto = {'menus': get_menus(user.username), 'usuario': usuario, 'user': user, }
    return render(request, 'app/vendedor_profile.html', context=info_producto)


def vendedor_profileAlumno1(request):
    return vendedor_profileAlumno(request, 'michaeljackson')


def vendedor_profileAlumno2(request):
    return vendedor_profileAlumno(request, 'ratatouille')


def vendedor_profileAlumno3(request):
    return vendedor_profileAlumno(request, 'pedropiedra')


def vendedor_profileAlumno4(request):
    return vendedor_profileAlumno(request, 'jorgegonzalez')


def vendedor_profileAlumno(request, usuario):
    clase_user = User.objects.get(username=usuario)
    clase_info = UserInfo.objects.get(user_id=clase_user.id)
    clase_vendedor = Vendedor.objects.get(userinfo_ptr_id=clase_user.id)
    horario = ''
    if 'fijo' in clase_info.tipo:
        clase_fijo = VendedorFijo.objects.get(vendedor_ptr_id=clase_user.id)
        tipo = 'Vendedor Fijo'
        horario = str(clase_fijo.apertura) + '-' + str(clase_fijo.cierre)
    else:
        clase_ambulante = VendedorAmbulante.objects.get(vendedor_ptr_id=clase_user.id)
        tipo = 'Vendedor Ambulante'
    formas_de_pago = []
    if clase_vendedor.efectivo == 1:
        formas_de_pago.append('Efectivo')
    if clase_vendedor.tarj_cred == 1:
        formas_de_pago.append('Tarjeta de Credito')
    if clase_vendedor.tarj_deb == 1:
        formas_de_pago.append('Tarjeta de Debito')
    if clase_vendedor.tarj_junaeb == 1:
        formas_de_pago.append('Tarjeta Junaeb')
    estado = 'No disponible'
    if clase_user.is_active:
        estado = 'Disponible'
        user = User.objects.filter(is_active=1)
    info_vendedor = {
        'nombre': clase_vendedor.nombre_visible,
        'tipo_vendedor': tipo,
        'estado': estado,
        'formas_de_pago': formas_de_pago,
        'menus': get_menus(usuario),
        'imagen': clase_vendedor.archivo_foto_perfil,
        'horario': horario,
        'user': usuario,
    }
    return render(request, 'app/vendedor_profileAlumno.html', context=info_vendedor)


def vendedor_edit(request):
    # formulario lleno, edicion de datos
    user = User.objects.get(is_active=1)

    if request.method == 'POST':
        form = EditVForm(request.POST)
        # obtengo mail y pass

        if form.is_valid():
            nombre = form.cleaned_data['name']

            if nombre != None:
                usuario = Vendedor.objects.get(user=user)
                usuario.nombre_visible = nombre
                usuario.save()
                if usuario.tipo == 'fijo':
                    usuario = VendedorFijo.objects.get(user=user)
                    return render(request, 'app/vendedor_profile.html',
                                  {'menus': get_menus(user.username), 'usuario': usuario, 'user': user})
                elif usuario.tipo == "ambulante":
                    usuario = VendedorAmbulante.objects.get(user=user)
                    return render(request, 'app/vendedor_profile.html',
                                  {'menus': get_menus(user.username), 'usuario': usuario, 'user': user})

        else:
            form = EditVForm()
            usuario = Vendedor.objects.get(user=user)
            return render(request, 'app/vendedor_edit.html', {'form': form, 'user': user, 'usuario': usuario})
    else:
        form = EditVForm()
        usuario = Vendedor.objects.get(user=user)
        return render(request, 'app/vendedor_edit.html', {'form': form, 'user': user, 'usuario': usuario})


def editar_producto(request):
    user = User.objects.get(is_active=1)
    productos = Productos.objects.filter(user=user.username)
    prod = []
    for i in productos:
        prod.append(i)
    return render(request, 'app/editar_producto.html', {'item': prod[0], 'user': user})


def iniciar():
    vendedor_profile()


def add_item(request):
    form = ProductForm(request.POST)
    print(form.errors)
    print(request.POST)
    if request.method == 'POST' and form.is_valid():
        username = User.objects.get(is_active=1)
        user = username.username
        nombre = form.cleaned_data['nombre']
        precio = form.cleaned_data['precio']
        stock = form.cleaned_data['stock']
        descripcion = form.cleaned_data['descripcion']
        categoria = form.cleaned_data['categoria']
        prod = Productos(user=user, nombre=nombre, precio=precio, stock=stock, descripcion=descripcion,
                         categoria=categoria)
        prod.save()
        return vendedor_profile(request)
    else:
        usuario = User.objects.get(is_active=1)
        user = User.objects.get(is_active=1)
        info_producto = {'menus': get_menus(user.username), 'usuario': usuario, 'user': user, 'form': form}
        return render(request, 'app/vendedor_profile.html', context=info_producto)
