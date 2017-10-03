# -*- coding: utf-8 -*-
if not auth.is_logged_in():
    redirect(URL('default','user/login'))

#@cache.action(time_expire=5, cache_model=cache.disk, quick='SV')
@cache(request.env.path_info,time_expire=5,cache_model=cache.ram)
def listaconsultas():
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
    total = db(db.consulta.auth_id == auth.user.id).count()
    consultas_per_page = 3
    pages = total / consultas_per_page
    if total%pages:
        consultas_per_page += 1
    start = (page-1)*consultas_per_page
    end = page*consultas_per_page
    response.flash = request.vars['mensagem'] or ''
    status = request.vars['f'] or 'Tudo'
    if status == 'Tudo':
        consultas = db(db.consulta.auth_id == auth.user.id).select(
            db.consulta.id,
            db.consulta.dataconsulta,
            db.consulta.status,
            db.consulta.motivo,
            db.consulta.endereco,
            db.consulta.cidade,
            db.consulta.auth_id,
            orderby=db.consulta.dataconsulta,
            limitby=(start,end),
            # left=db.resultadoconsulta.on(
                # db.consulta.id == db.resultadoconsulta.consulta_id),
        #    groupby=db.consulta.id
        )
    else:
        consultas = db((db.consulta.auth_id == auth.user.id) &
                       (db.consulta.status == status)).select(
            db.consulta.id,
            db.consulta.dataconsulta,
            db.consulta.status,
            db.consulta.motivo,
            db.consulta.endereco,
            db.consulta.cidade,
            db.consulta.auth_id,
            orderby=db.consulta.dataconsulta,
            limitby=(start,end),
            # left=db.resultadoconsulta.on(
                # db.consulta.id == db.resultadoconsulta.consulta_id)
        )
    grupos = [ 'Tudo','Criada','Marcada','Realizada' ]

    return response.render("consultas/listaconsultas.html",
            dict(consultas = consultas, grupos=grupos, status=status,
            page=page, pages=pages))

def nova():
    form = SQLFORM(db.consulta)
    form.vars.auth_id = auth.user.id
    form.element('textarea[name=descricao]')['_style'] = 'height:50px;'
    dbperfil = TR(INPUT(_name='dbperfil',value='consulta',_type='hidden'))
    form[0].insert(-1,dbperfil)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect( request.env.http_web2py_component_location,client_side=True)

    elif form.errors:
        response.flash = 'Verifique os erros'
    # else:
        # response.flash = 'Preencha o fornulário'
    return dict(form=form)

def edita():
    consulta_id = request.vars['c']
    if db(db.consulta.id == consulta_id).select().first().auth_id != auth.user.id:
        response.flash = 'Consulta não pertence a esse paciente'
        redirect(URL('listaconsultas',vars={'mensagem': response.flash}))
    consulta = db(db.consulta.id == consulta_id).select().first()
    form = SQLFORM(db.consulta, consulta)
    dbperfil = TR(INPUT(_name='dbperfil',value='consulta',_type='hidden'))
    form[0].insert(-1,dbperfil)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('consultas','listaconsultas.html'))
    elif form.errors:
        response.flash = 'Verifique os erros'
    else:
        response.flash = 'Preencha o fornulário'
    return dict(form=form)

def editaresultado():
    resultado_id = request.vars['r']
    '''if db(db.resultadoconsulta.id == resultado_id).select().first().auth_id != auth.user.id:
        response.flash = 'Resultado não pertence a esse paciente'
        redirect(URL('listaresultadosconsultas',vars={'mensagem': response.flash}))'''
    resultado = db(db.resultadoconsulta.id == resultado_id).select().first()
    form = SQLFORM(db.resultadoconsulta, resultado, upload=URL('download'), deletable=True)
    form.element('textarea[name=resultado]')['_style'] = 'width:150px;height:50px;'
    if form.process().accepted:
        response.flash = 'form accepted'
        if request.vars.reload_div:
            print "request.vars.reload_div: " + str(request.vars.reload_div)
            response.js =  "jQuery('#%s').get(0).reload()" % request.vars.reload_div
        redirect(URL('consultas','listaconsultas.html'))
    elif form.errors:
        response.flash = 'Verifique os erros'
    return dict(form=form)

def footer_consulta_lista_resultados():
    consulta = request.vars['c']
    resultados = db((db.resultadoconsulta.consulta_id == consulta)).select()
    resultados_mensagem = None
    if len(resultados) == 0:
        resultados_mensagem = 'Não possui resultados'
    return response.render('consultas/footer_consulta_lista_resultados.load',
            dict(resultados=resultados, consulta = consulta, resultados_mensagem=resultados_mensagem))

def footer_consulta_novo_resultado():
    consulta = request.vars['c']
    motivoconsutla = db(db.consulta.id == consulta).select().first().motivo
    form = SQLFORM(db.resultadoconsulta, upload=URL('download'),_id='form_novo_resultado')
    form.vars.consulta_id = consulta
    form.vars.auth_id = auth.user.id
    form.element('textarea[name=resultado]')['_style'] = 'width:150px;height:50px;'
    if form.process().accepted:
        response.flash = 'Novo resultado da consulta "%s" criado!' %(motivoconsutla)
        if request.vars.reload_div:
            print request.vars.reload_div
            response.js =  "jQuery('#%s').get(0).reload()" % request.vars.reload_div
    elif form.errors:
        response.flash = 'Verifique os erros!'
    # else:
    #     response.flash = 'Preencha o formulário'
    return dict(form = form)

def footer_consulta_lista_exames():
    consulta = request.vars.c
    exames = db(db.exame.consulta_id == consulta).select()
    exames_mensagem = None
    if len(exames) == 0:
        exames_mensagem = 'Não possui exames'
    return response.render('consultas/footer_consulta_lista_exames.load',
                dict(exames = exames, consulta = consulta, exames_mensagem = exames_mensagem))

def footer_consulta_novo_exame():
    consulta = request.vars['c']
    db.exame.auth_id.default = auth.user.id
    db.exame.consulta_id.default = consulta
    form = SQLFORM(db.exame, upload=URL('download'),_id='form_novo_exame')
    form.vars.consulta_id = consulta
    form.vars.auth_id = auth.user.id
    form.element('textarea[name=descricao]')['_style'] = 'width:150px;height:50px;'
    dbperfil = TR(INPUT(_name='dbperfil',value='exame',_type='hidden'))
    form[0].insert(-1,dbperfil)
    if form.process().accepted:
        response.flash = 'Novo exame da consulta %s criado!' %(str(consulta))
        if request.vars.reload_div:
            print request.vars.reload_div
            response.js =  "jQuery('#%s').get(0).reload()" % request.vars.reload_div
    elif form.errors:
        response.flash = 'Verifique os erros!'
    return dict(form = form)

def editaexame():
    exame_id = request.vars['e']
    '''if db(db.resultadoexames.id == exame_id).select().first().auth_id != auth.user.id:
        response.flash = 'Resultado não pertence a esse paciente'
        redirect(URL('listaresultadosconsultas',vars={'mensagem': response.flash}))'''
    exame = db(db.exame.id == exame_id).select().first()
    form = SQLFORM(db.exame, exame, upload=URL('download'), deletable=True)
    #form.element('textarea[name=resultado]')['_style'] = 'width:150px;height:50px;'
    dbperfil = TR(INPUT(_name='dbperfil',value='exame',_type='hidden'))
    form[0].insert(-1,dbperfil)
    if form.process().accepted:
        response.flash = 'Novo exame salvo !'
        if request.vars.reload_div:
            print "request.vars.reload_div: " + str(request.vars.reload_div)
            response.js =  "jQuery('#%s').get(0).reload()" % request.vars.reload_div
        redirect(URL('consultas','listaconsultas.html'))

    elif form.errors:
        response.flash = 'Verifique os erros'
    return dict(form=form)


def editaresultadoexame():
    exame_id = request.vars['e']
    '''if db(db.resultadoexames.id == exame_id).select().first().auth_id != auth.user.id:
        response.flash = 'Resultado não pertence a esse paciente'
        redirect(URL('listaresultadosconsultas',vars={'mensagem': response.flash}))'''
    exame = db(db.resultadoexames.id == exame_id).select().first()
    form = SQLFORM(db.resultadoexames, exame, upload=URL('download'), deletable=True)
    form.element('textarea[name=resultado]')['_style'] = 'width:150px;height:50px;'
    if form.process().accepted:
        response.flash = 'Novo exame salvo !'
        if request.vars.reload_div:
            print "request.vars.reload_div: " + str(request.vars.reload_div)
            response.js =  "jQuery('#%s').get(0).reload()" % request.vars.reload_div

    elif form.errors:
        response.flash = 'Verifique os erros'
    return dict(form=form)
