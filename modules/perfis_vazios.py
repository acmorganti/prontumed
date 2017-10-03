# -*- coding: utf-8 -*-
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


def endereco_vazio(endereco):
    if endereco == None:
        return True
    if endereco.nome_endereco == None or \
       endereco.cep == None or \
       endereco.endereco == None or \
       endereco.numero == None or \
       endereco.mplemento == None or \
       endereco.estado == None:
        return True
    else:
        return False
