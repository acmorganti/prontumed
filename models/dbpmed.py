import datetime
states = ['Acre',
            'Alagoas',
            'Amapá',
            'Amazonas',
            'Bahia',
            'Ceará',
            'Distrito Federal',
            'Espírito Santo',
            'Goiás',
            'Maranhão',
            'Mato Grosso',
            'Mato Grosso do Sul',
            'Minas Gerais',
            'Pará',
            'Paraíba',
            'Paraná',
            'Pernambuco',
            'Piauí',
            'Rio de Janeiro',
            'Rio Grande do Norte',
            'Rio Grande do Sul',
            'Rondônia',
            'Roraima',
            'Santa Catarina',
            'São Paulo',
            'Sergipe',
            'Tocantins',
            ]

db.define_table(
    'patient',
    Field('auth_id','reference auth_user'),
    Field('nome','string',length=100,default=None),
    Field('nome_mae', 'string',length=100,default=None,label='Nome Mãe'),
    Field('nome_pai', 'string',length=100,default=None,label='Nome Pai'),
    Field('contato', 'string', length=100,default=None),
    Field('fone_contato','string',length=11,default=None,label='Fone Contato'),
    Field('fone_fixo','string',length=11,default=None,label='Fone Fixo'),
    Field('fone_celular','string',length=11,default=None,label='Fone Celular'),
    Field('dt_nascimento','date',default=None,label='Data Nascimento'),
    Field('sexo','string',length=10,default=None,label='Sexo',requires=IS_EMPTY_OR(IS_IN_SET(['Feminino','Masculino']))),
    Field('profissao','string',length=100,default=None,label='Profissão'),
    Field('status','string',length=10,requires=IS_IN_SET(['Demo','Ativo','Inativo']),default='demo'),
    auth.signature,
)

db.define_table(
    'medical_profile',
    Field('auth_id','reference auth_user'),
    Field('alergia','text',default=None,label='Possui alguma alergia?'),
    Field('coracao','text',default=None,label='Problemas no Coração?'),
    Field('glutten','boolean',default=None,label='Intolerância a Glutten?'),
    Field('lactose','boolean',default=None,label='Intolerância a Lactose?'),
    Field('deficiencia','text',default=None,label='Apresenta alguma deficiência?'),
    Field('desmaio','text',default=None,label='Já teve ou costuam ter desmaios?'),
    Field('medicacao','text',default=None,label='Utiliza alguam medicação?'),
    Field('diabetes','boolean',default=None,label='Apresenta diabetes?'),
    Field('tratadiabetes','text',default=None,label='Caso de diates, qual tratamento faz?'),
    Field('coluna','text',default=None,label='Problemas de coluna?'),
    Field('fratura','text',default=None,label='Já teve ou possui alguma fratura?'),
    Field('cirurgia','text',default=None,label='Já teve alguma cirurgia?'),
    Field('peso','float',default=None,label='Problemas com obesidade?'),
    Field('tratamento','text',label='Faz alguma tratamento específico?'),
    Field('vacina','text',label='Vacinas?',default=None),
    auth.signature,
)

db.define_table(
    'endereco',
    Field('auth_id','reference auth_user'),
    Field('nome_endereco','string', length=100, label='Nome do Endereço', default=None),
    Field('cep','string',length=8,default=None, label='CEP'),
    Field('endereco','string',length=200,default=None, label='Endereço'),
    Field('numero','integer',default=None, label='Número'),
    Field('complemento','string',length=200,default=None, label='Complemento'),
    Field('bairro','string',length=200,default=None,label='Bairro',),
    Field('cidade','string',length=200,default=None,label='Cidade'),
    Field('estado','string',default=None, requires=IS_IN_SET(states), label='Estado'),
)

db.define_table(
    'consulta',
    Field('auth_id','reference auth_user',writable=False, readable=False),
    Field('motivo','string',length=200, default=None,label='Motivo'),
    Field('descricao','text',default=None,label='Descrição'),
    Field('medico',label='Nome Médico',default=None),
    Field('especialidade',label='Especialidade', default=None),
    Field('crm',label='CRM', default=None),
    Field('dataconsulta','datetime', label='Data Consulta',default=None),
    Field('cep','string',length=8,default=None, label='CEP'),
    Field('endereco',label='Endereço',default=None),
    Field('bairro','string',length=200,default=None,label='Bairro',),
    Field('cidade','string',length=200,default=None,label='Cidade'),
    Field('estado', requires=IS_EMPTY_OR(IS_IN_SET(states)),default=None),
    Field('fone','string',label='Fone Médico',default=None),
    Field('status','string',length=15,label='Situação',default='Criada',
            requires=IS_IN_SET(['Criada','Marcada','Realizada'])),
    auth.signature,
)

db.define_table(
    'resultadoconsulta',
    Field('auth_id','reference auth_user',writable=False, readable=False),
    Field('consulta_id','reference consulta',writable=False, readable=False),
    Field('resultado','text',label='Descrição Resultado Consulta',default=None),
    Field('receita','upload',label='Foto Receita',default=None),
    auth.signature
)

db.define_table(
    'exame',
    Field('auth_id', 'reference auth_user'),
    Field('consulta_id','reference consulta',),
    Field('exame', 'string', length=200,default=None),
    Field('descricao', 'text', default=None, label='Descrição' ),
    Field('dataeexame','datetime', label='Data Exame',default=None),
    Field('cep','string',length=8,default=None, label='CEP'),
    Field('endereco',label='Endereço',default=None),
    Field('bairro','string',length=200,default=None,label='Bairro',),
    Field('cidade','string',length=200,default=None,label='Cidade'),
    Field('estado', requires=IS_EMPTY_OR(IS_IN_SET(states)),default=None),
    Field('fone','string',label='Fone Médico',default=None),
    Field('status','string',length=15,label='Situação',default='Criada',
        requires=IS_IN_SET(['Criada','Marcada','Realizada'])),
    auth.signature,
)

db.define_table(
    'dbexame',
    Field('auth_id', 'reference auth_user'),
    Field('consulta_id','reference consulta',),
    Field('exame', 'string', length=200,default=None),
    Field('descricao', 'text', default=None, label='Descrição' ),
    Field('dataeexame','datetime', label='Data Exame',default=None),
    Field('endereco',label='Endereço',default=None),
    Field('cidade',label='Cidade',default=None),
    Field('estado', requires=IS_EMPTY_OR(IS_IN_SET(states)),default=None),
    Field('fone','string',label='Fone Médico',default=None),
    Field('status','string',length=15,label='Situação',default=None,requires=IS_IN_SET(['Criada','Marcada','Realizada'])),
    auth.signature,
)

db.define_table(
    'resultadoexames',
    Field('auth_id','reference auth_user'),
    Field('exame_id', 'reference exame'),
    Field('resultado','text',label='Resultado',default=None),
    Field('imagem','upload',label='Imagem',default=None),
    auth.signature
)
db.define_table(
    'teste_api',
    Field('resultado','text'),
    Field('ra','text'),
    Field('rv','text'),
    )

db.define_table(
    'plano',
    Field('plano','string',length=10),
    Field('valor','float'),
    Field('tempo','integer'),
    Field('valor_format',compute = lambda r: ("%.2f" % round(r['valor'],2))),
    format='%(plano)s'
)
db.define_table(
    'assinatura',
    Field('auth_id',db.auth_user),
    Field('plano_id',db.plano,
            requires=IS_EMPTY_OR(IS_IN_DB(db,'plano.id','%(plano)s - R$%(valor_format)s',zero='Escolha um dos planos:'))),
    Field('dt_vencimento','date',label='Data Vencimento',default=datetime.date.today()),
    Field('status','string',length=10,requires=IS_EMPTY_OR(IS_IN_SET(['Ativo','Inativo']))),
    auth.signature,
)

db.define_table(
    'fatura',
    Field('auth_id', 'reference auth_user'),
    Field('dt_vencimento','date',label='Data Vencimento',default=datetime.date.today()),
    Field('plano',db.plano,
           requires=IS_IN_DB(db,'plano.id','%(plano)s - R$%(valor_format)s',zero='Escolha um dos planos:')),
    Field('status','string',requires=IS_IN_SET(['Aberto','Pago','Em atraso','Cancelado']),
            writable=False, default='Aberto'),
    Field('prox_vencimento',compute = lambda r:
      r['dt_vencimento'] + datetime.timedelta(days=30)),
    auth.signature,
)

db.define_table(
    'api_pagamento',
    Field('id_transacao','string',length=32),
    Field('valor','integer'),
    Field('status_pagamento','integer'),
    Field('cod_moip','string',length=20),
    Field('tipo_pagamento','string',length=32),
    Field('email_consumidor','string',length=45),
)

db.define_table(
    'resposta_recebimento',
    Field('id_transacao','string',length=32),
    Field('valor','string',length=9),
    Field('status_pagamento','integer'),
    Field('cod_moit','string',length=20),
    Field('forma_pagamento','integer'),
    Field('tipo_pagamento','string',length=32),
    Field('email_consumidor','string',length=45)
)
