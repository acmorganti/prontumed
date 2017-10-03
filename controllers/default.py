# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import requests
import json
import datetime

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome!")
    return dict(message=T('Welcome to Prontumed!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    auth.settings.login_next = URL('default','inicio')
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

@auth.requires_login()
def inicio():
    print 'entrei no inicio'
    response.flash = 'IMPORTANTE! Complete seu cadastro:'
    patient = db(db.patient.auth_id == auth.user.id).select().first()
    medical_profile = db(db.medical_profile.auth_id == auth.user.id).select().first()
    endereco = db(db.endereco.auth_id == auth.user.id).select().first()
    if patient_vazio(patient):
        response.flash += ' - dados pessoais -'
        vvars = {'perfil': 'patient', 'responseflash': response.flash}
    if medical_profile_vazio(medical_profile):
        response.flash += ' dados médicos -'
        vvars = {'perfil': 'medical_profile', 'responseflash': response.flash}
    if endereco_vazio(endereco):
        response.flash += ' endereço -'
        vvars = {'perfil': 'endereco', 'responseflash': response.flash}
    if response.flash == 'IMPORTANTE! Complete seu cadastro:':
        response.flash = ''
        redirect(URL('consultas','listaconsultas'))
    redirect(URL('man_perfis', vars=vvars))
    return dict()

@auth.requires_login()
def apos_registro():
    mail.send(auth.user.email,
              'Bem vindo!',
              '<html><h1>Seja bem vindo à Prontumed!</h1><p>A partir de agora você tem todas as suas informações médicas de onde estiver.<br>Tenha acesso a sua ficha médica, o histórico de suas consultas e exames.<br>Nunca sabemos quando teremos problemas, imagine numa viagem e precisa de socorro. Com a Prontumed, o médico que te atender saberá todo o seu histórico e dará a melhor orientação.Saiba que aqui há humanos trabalhando por você. Sempre que precisar de ajuda, entre em contato em:<br><br><strong>suporte@prontumed.com</strong><br><br>Att<br><br><spam style="color: green"><strong>Prontumed.com</strong></span></p></html>')
    redirect(URL('man_perfis',vars={'perfil':'patient'}))
    return dict()

@auth.requires_login()
def man_perfis():
    if db(db.assinatura.auth_id == auth.user.id).count() == 0:
        db.assinatura.insert(
            auth_id = auth.user.id,
            plano_id = None,
            dt_vencimento=datetime.date.today() + datetime.timedelta(days=30),
            status = 'Ativo'
        )
        db.commit()
    response.flash = request.vars['responseflash']
    table=db[request.vars['perfil']]
    tables = { 'patient': 'Dados Pessoais',
               'medical_profile': 'Dados Médicos',
               'endereco': 'Endereço'}
    perfil = db(table.auth_id == auth.user.id)
    if perfil.count() == 0:
        perfil = table.insert(auth_id = auth.user.id)
        db.commit()
        perfil = db(table.auth_id == auth.user.id)
    form = SQLFORM(table, perfil.select().first())
    dbperfil = TR(INPUT(_name='dbperfil',value=table,_type='hidden'))
    form[0].insert(-1,dbperfil)
    if form.process().accepted:
        response.flash='Perfil salvo'
    elif form.errors:
        response.flash='Verifique as informações do seu perfil'
    return dict(form=form, nome_perfil = tables[request.vars['perfil']], mensagem = response.flash)

@auth.requires_login()
def patient_vazio(patient):
    if patient == None:
        return True
    if patient.nome == None or \
       patient.nome_pai == None or \
       patient.nome_mae == None or \
       patient.contato == None or \
       patient.fone_contato == None or \
       patient.fone_fixo == None or \
       patient.fone_celular == None or \
       patient.dt_nascimento == None or \
       patient.sexo == None or \
       patient.profissao == None:
        return True
    else:
        return False

@auth.requires_login()
def medical_profile_vazio(medical_profile):
    if medical_profile == None:
        return True
    if medical_profile.alergia == None or \
       medical_profile.coracao == None or \
       medical_profile.glutten == None or \
       medical_profile.lactose == None or \
       medical_profile.deficiencia == None or \
       medical_profile.desmaio == None or \
       medical_profile.medicacao == None or \
       medical_profile.diabetes == None or \
       medical_profile.tratadiabetes == None or \
       medical_profile.coluna == None or \
       medical_profile.fratura == None or \
       medical_profile.cirurgia == None or \
       medical_profile.peso == None or \
       medical_profile.tratamento == None or \
       medical_profile.vacina == None:
        return True
    else:
        return False

@auth.requires_login()
def endereco_vazio(endereco):
    if endereco == None:
        return True
    if endereco.nome_endereco == None or \
       endereco.cep == None or \
       endereco.endereco == None or \
       endereco.numero == None or \
       endereco.complemento == None or \
       endereco.estado == None:
        return True
    else:
        return False

def preenche_cep():
    cep = request.vars.cep
    if len(cep) == 0:
    	return ''
    cep = cep.replace('-','')
    r = requests.get('https://viacep.com.br/ws/'+str(cep)+'/json/')
    resultado = json.loads(r.content)
    session.cep = resultado

    retorno =  "jQuery('#endereco_endereco').val(%s);" % repr(session.cep['logradouro'].encode('latin_1'))
    retorno += "jQuery('#endereco_bairro').val(%s);" % repr(session.cep['bairro'].encode('latin_1'))
    retorno += "jQuery('#endereco_cidade').val(%s);" % repr(session.cep['localidade'].encode('latin_1'))
    retorno += "jQuery('#endereco_complemento').val(%s);" % repr(session.cep['complemento'].encode('latin_1'))
    retorno += "jQuery('#endereco_cep').val(%s);" % repr(cep)
    retorno += comp_cep_estado()

    return retorno

def comp_cep_estado():
	uf = {'AC':'Acre',
          'AL':'Alagoas',
          'AP':'Amapá',
          'AM':'Amazonas',
          'BA':'Bahia',
          'CE':'Ceará',
          'DF':'Distrito Federal',
          'ES':'Espírito Santo',
          'GO':'Goiás',
          'MA':'Maranhão',
          'MT':'Mato Grosso',
          'MS':'Mato Grosso do Sul',
          'MG':'Minas Gerais',
          'PA':'Pará',
          'PB':'Paraíba',
          'PR':'Paraná',
          'PE':'Pernambuco',
          'PI':'Piauí',
          'RJ':'Rio de Janeiro',
          'RN':'Rio Grande do Norte',
          'RS':'Rio Grande do Sul',
          'RO':'Rondônia',
          'RR':'Roraima',
          'SC':'Santa Catarina',
          'SP':'São Paulo',
          'SE':'Sergipe',
          'TO':'Tocantins',}
	x = uf[session.cep['uf']]
	retorno =  "jQuery('#endereco_estado').val(%s);" % repr(x.decode('utf-8)').encode('latin_1'))
	return retorno
