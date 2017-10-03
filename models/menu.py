# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(IMG(_src=URL('static','/images/logo.png')),
                  _class="navbar-brand", _href=URL('default','index'),
                  _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

if auth.is_logged_in():
    response.menu = [
        (T('Home'), False, URL('default', 'index'), [],),
        ('Perfil', False, 'Perfil',[['Dados Pessoais', False, URL('default','man_perfis', vars={'perfil': 'patient'})],
                                     ['Dados Médicos', False, URL('default','man_perfis', vars={'perfil': 'medical_profile'})],
                                     ['Endereço', False, URL('default','man_perfis', vars={'perfil': 'endereco'})],],
        ),
        (T('Consultas/Exames'), False, URL('consultas', 'listaconsultas',vars=dict(page=1)), [],),
        (T('Blog'), False, URL('blog', 'index'), [],),
        (T('Assinatura'), False, URL('assinatura', 'index'), [],),
        ]
else:
    response.menu = [
        (T('Home'), False, URL('default', 'index'), [],),
        (T('Blog'), False, URL('blog', 'index'), [],),
        ]





DEVELOPMENT_MENU = False


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------



if "auth" in locals():
    auth.wikimenu()
