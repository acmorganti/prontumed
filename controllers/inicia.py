# -*- coding: utf-8 -*-
import datetime
import random
def create_db():
	# inicia usuarios
	mensagem = [ "Limpando tabelas" ]
	tabelas = [ 'patient', 'consulta', 'medical_profile', 'endereco', 'exame', 'resultadoconsulta']
	for tabela in tabelas:
		db.executesql("delete from %s;" %(tabela))
		db.executesql("delete from sqlite_sequence where name='%s';" %(tabela))
	db.commit()

	# inicia usuarios:
	'''mensagem.append( '--- Inserindo usuários ---')
	db.auth_user.insert(email='teste1@teste.com',password='123456')
	db.auth_user.insert(email='teste2@teste.com',password='123456')
	db.auth_user.insert(email='teste3@teste.com',password='123456')
	db.auth_user.insert(email='teste4@teste.com',password='123456')
	db.auth_user.insert(email='teste5@teste.com',password='123456')
	db.commit()
	mensagem.append('--- %s Usuários inseridos ---' %(str(db(db.auth_user).count())))'''
	# inicia patient

	db.plano.insert(plano="Mensal", valor=7.00)
	db.plano.insert(plano="Anual", valor=50.00)
	db.commit()

	mensagem.append( '--- Inserindo perfis paciente, médico e endereço ---')
	sexo = 'Masculino'
	glutten = True
	lactose = True
	diabetes = True
	tratadiabetes = True
	for a in db(db.auth_user).select():
		sexo = 'Feminino' if sexo == 'Masculino' else 'Masculino'
		db.patient.insert( auth_id = a.id,
							nome = a.email,
							nome_mae = 'mae %s' %(str(a.id)),
							nome_pai = 'pai %s' %(str(a.id)),
							contato = 'contato %s' %(str(a.id)),
							fone_contato = '11999999999',
							fone_fixo = '11999999999',
							fone_celular = '11999999999',
							dt_nascimento = datetime.date(2001, 1, 1),
							sexo = sexo,
							profissao = 'teste profissao'
						)
		glutten = True if glutten == False else True
		lactose = True if lactose == False else True
		diabetes = True if diabetes == False else True
		tratadiabetes = True if tratadiabetes == False else True
		db.medical_profile.insert( auth_id = a.id,
									alergia = 'teste alergia %s' %(str(a.id)),
									coracao = 'teste coracao',
									glutten = glutten,
									lactose = lactose,
									deficiencia = 'teste de deficiencia',
									desmaio = 'teste de desmaio',
									medicacao = 'teste de medicacao',
									diabetes = diabetes,
									tratadiabetes = tratadiabetes,
									coluna = 'teste de coluna',
									fratura = 'teste de fratura',
									cirurgia = 'teste de cirurgia',
									peso = 65.5,
									tratamento = 'teste de tratamento',
									vacina = 'teste de vacina',
						)
		db.endereco.insert( auth_id = a.id,
							nome_endereco = 'teste endereco',
							cep = '00000-000',
							endereco = 'teste de endereco',
							numero = '100',
							complemento = 'teste de complemento',
							estado = 'São Paulo',
						)
	db.commit()
	mensagem.append( '--- %s Perfis inseridos ---' %(str(db(db.patient).count())))
	mensagem.append( '--- inserindo consultas ---')
	status = 'Realizada'
	for a in db(db.auth_user).select():
		dataconsulta = datetime.date(2017,10,1)
		for q in range(1,random.randint(1,10)):
			if status == 'Realizada':
				status = 'Criada'
			elif status == 'Criada':
				status = 'Marcada'
			elif status == 'Marcada':
				status = 'Realizada'
			db.consulta.insert( auth_id = a.id,
							motivo = 'Consulta %s do usuario %s' %(str(q), str(a.id)),
							descricao = 'Descrição da consulta %s do usuario %s' %(str(q), str(a.id)),
							medico = 'Médico da consulta %s do usuario %s' %(str(q), str(a.id)),
							especialidade = 'Especialidade da consulta %s do usuario %s' %(str(q), str(a.id)),
							crm = '101010',
							dataconsulta = dataconsulta,
							endereco = 'Endereco da consulta %s do usuario %s' %(str(q), str(a.id)),
							cidade = 'Cidade da consulta %s do usuario %s' %(str(q), str(a.id)),
							estado = 'Estado da consulta %s do usuario %s' %(str(q), str(a.id)),
							fone = '11999999999',
							status = status,
							)
			dataconsulta = dataconsulta + datetime.timedelta(days = 30)
	db.commit()
	mensagem.append( '--- %s consultas inseridas ---' %(str(db(db.consulta).count())))
	mensagem.append( '--- inserindo resultado das consultas ---')
	for a in db(db.consulta).select():
		for x in range(0,random.randint(1,5)):
			if a.status == 'Realizada':
				db.resultadoconsulta.insert(
							auth_id = a.auth_id,
							consulta_id = a.id,
							resultado = 'Resultado %s da consulta %s do usuario %s' %(str(x),str(a.id), str(a.auth_id)),
							receita = 'Receita da consulta %s do usuario %s' %(str(a.id), str(a.auth_id)),
							)
	db.commit()
	mensagem.append( '--- %s resultados das consultas inseridos ---' %(str(db(db.resultadoconsulta).count())))
	status = 'Realizada'
	dataeexame = datetime.date(2017,10,15)
	for a in db(db.consulta).select():
		if status == 'Realizada':
			status = 'Criada'
		elif status == 'Criada':
			status = 'Marcada'
		elif status == 'Marcada':
			status = 'Realizada'
		if a.status == 'Realizada':
			db.exame.insert(
						auth_id = a.auth_id,
						consulta_id = a.id,
						exame = 'Exame da consulta %s do usuario %s' %(str(a.id),str(a.auth_id)),
						descricao = 'Descrição do exame da consulta %s do usuario %s' %(str(a.id),str(a.auth_id)),
						dataeexame = dataeexame,
						endereco = 'Endereço do exame da consulta %s do usuario %s' %(str(a.id),str(a.auth_id)),
						cidade = 'Cidade do exame da consulta %s do usuario %s' %(str(a.id),str(a.auth_id)),
						estado = 'São Paulo',
						fone = '11999999999',
						status = status,
		)
		dataeexame = dataeexame + datetime.timedelta(days = 30)
	db.commit()
	mensagem.append( '--- %s exames criados ---' %(str(db(db.exame).count())))
	for a in db(db.exame).select():
		for x in range(1,random.randint(1,5)):
			db.resultadoexames.insert(
									auth_id = a.auth_id,
									exame_id = a.id,
									resultado = 'Resultado %s do exame %s do usuario %s' %(str(x),str(a.id),str(a.auth_id)),
									)
	db.commit()
	mensagem.append( '--- %s resultado dos exames criados ---' %(str(db(db.resultadoexames).count())))
	return dict(mensagem = mensagem)
