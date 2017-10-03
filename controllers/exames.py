# -*- coding: utf-8 -*-
if not auth.is_logged_in():
    redirect(URL('default','user/login'))

def footer_consulta_lista_exames():
    consulta = request.vars.c
    exames = db(db.exame.consulta_id == consulta).select()
    exames_mensagem = None
    if len(exames) == 0:
        exames_mensagem = 'Não possui exames'
    return dict(exames = exames, consulta = consulta, exames_mensagem = exames_mensagem)

def footer_consulta_novo_exame():
    consulta = request.vars['c']
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
    dbperfil = TR(INPUT(_name='dbperfil',value='exame',_type='hidden'))
    form[0].insert(-1,dbperfil)
    #form.element('textarea[name=resultado]')['_style'] = 'width:150px;height:50px;'
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
