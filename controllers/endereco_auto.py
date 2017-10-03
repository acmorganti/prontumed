# -*- coding: utf-8 -*-
import requests
import json

def preenche_cep():
    cep = request.vars.cep[0]
    table = request.vars.dbperfil[0]
    print cep
    print table
    if len(cep) == 0:
    	return ''
    cep = cep.replace('-','')
    r = requests.get('https://viacep.com.br/ws/'+str(cep)+'/json/')
    resultado = json.loads(r.content)
    session.cep = resultado
    retorno =  "jQuery('#%s_endereco').val(%s);" % (table, repr(session.cep['logradouro'].encode('latin_1')))
    print retorno

    retorno += "jQuery('#%s_bairro').val(%s);" % (table, repr(session.cep['bairro'].encode('latin_1')))
    retorno += "jQuery('#%s_cidade').val(%s);" % (table, repr(session.cep['localidade'].encode('latin_1')))
    retorno += "jQuery('#%s_complemento').val(%s);" % (table, repr(session.cep['complemento'].encode('latin_1')))
    retorno += "jQuery('#%s_cep').val(%s);" % (table, repr(cep))
    retorno += comp_cep_estado(table)

    return retorno

def comp_cep_estado(table):
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
	retorno =  "jQuery('#%s_estado').val(%s);" % (table, repr(x.decode('utf-8)').encode('latin_1')))
	print 'estado: '+retorno
	return retorno
