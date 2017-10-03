# -*- coding: utf-8 -*-
import datetime

@auth.requires_login()
def index():
    faturas = db(db.fatura.auth_id == auth.user.id).select()
    assinatura = db(db.assinatura.auth_id == auth.user.id).select().first()
    return dict(faturas=faturas, assinatura=assinatura)


@auth.requires_login()
def new():
    form = SQLFORM(db.fatura,submit_button='Pagar')
    form.vars.auth_id = auth.user.id
    if form.process().accepted:
        fatura_id=form.vars.id
        redirect(URL('paga',vars={'fatura_id': fatura_id}))
        response.flash = 'Fatura %s criada!' %(str(vid))
    elif form.errors:
        response.flash = 'Verificar os erros'
    return dict(form = form)

@auth.requires_login()
def paga():
    fatura_id = request.vars.fatura_id
    fatura = db(db.fatura.id == fatura_id).select().first()
    url_moip = 'https://desenvolvedor.moip.com.br/sandbox/PagamentoMoIP.do'
    id_carteira = 'acmorganti@gmail.com'
    plano_valor = db(db.plano.id == fatura.plano).select().first().valor
    valor = ("%.2f" % round(plano_valor,2))
    valor = valor.replace(".","")
    nome = "Assinatura mensal do Prontumed - Prontuário médico online"
    descricao = "Assinatura do plano mensal da Prontumed"
    id_transacao = 'FAT%s' %(str(fatura_id))

    url_moip += '?'
    url_moip += 'id_carteira=%s' %(id_carteira)
    url_moip += '&valor=%s' %(valor)
    url_moip += '&nome=%s' %(nome)
    url_moip += '&descricao=%s' %(descricao)
    url_moip += '&id_transacao=%s' %(id_transacao)

    redirect(url_moip)
    return dict()

#?id_transacao=16&valor=700&status_pagamento=1&cod_moit=1&forma_pagamento=73&tipo_pagamento=BoletoBancario&email_consumidor='acmorganti@gmail.com'

def retorno():
    db.resposta_recebimento.insert(
        id_transacao = request.vars.id_transacao,
        valor = request.vars.valor,
        status_pagamento = request.vars.status_pagamento,
        cod_moit = request.vars.cod_moit,
        forma_pagamento = request.vars.forma_pagamento,
        tipo_pagamento = request.vars.tipo_pagamento,
        email_consumidor = request.vars.email_consumidor,
    )
    db.commit()
    id_transacao = request.vars.id_transacao[3:]
    fatura_id = int(id_transacao)
    fatura = db(db.fatura.id == fatura_id).select().first()
    assinatura = db(db.assinatura.auth_id == fatura.auth_id).select().first()
    if int(request.vars.status_pagamento) == 1:
        fatura.update_record(status = 'Pago')
        tempo = db(db.plano.id==fatura.plano).select().first().tempo
        assinatura.update_record(plano_id = fatura.plano,
                                dt_vencimento = datetime.date.today() + datetime.timedelta(days=tempo),
                                status = 'Ativo',
                                )
        titulo = 'Pagamento Recebido! Muito Obrigado'
        mensagem = 'Agradecemos o pagamento realizado'
    elif request.vars.status_pagamento == 5:
        fatura.update_record(status = 'Cancelado')
        assinatura.update_record(status='Inativo')
        titulo = 'Pagamento cancelado'
        mensagem = 'Seu pagamento foi cancelado na plataforma de pagamentos.'
    db.commit()

    email=db(db.auth_user.id == fatura.auth_id).select().first().email

    mail.send(email,titulo,mensagem)
    return dict()
