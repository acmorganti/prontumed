def recebedor():
    resposta = request.vars
    meurec = dict(trans_cod = resposta.trans_cod,
                  product_cod= resposta.product_cod,
                  cus_email = resposta.cus_email,
                  trans_status = resposta.trans_status,
                  cus_cod = resposta.cus_cod
                  )
    '''<Storage {'trans_createdate': '2017-09-26 10:01:48', 'page_checkout_url': 'http://g.eduzz.com/0000', 'aff_email': '', 'utm_content': 'utm_content', 'trans_cod': '1', 'product_cod': '1234',
'tracker_trk2': '456', 'tracker_trk3': '789', 'cus_address_state': 'SP', 'cus_tel': '15-33333-3333', 'tracker_trk': '123',
'billet_url': 'http://g.eduzz.com/checkout/boleto/000000-AAAAAA-AAAAAA-AAAAAA', 'cus_address_district': '', 'utm_campaign': 'utm_campaign', 'aff_cod': '', 'cus_tel2': '15-33333-3333',
'aff_value': '', 'utm_medium': 'utm_medium', 'cus_name': 'Cliente Teste', 'trans_paid': '0.00', 'api_key': '4babcd6938', 'product_name': 'Produto Teste', 'cus_address_zip_code': '',
 'cus_address_country': 'BR', 'cus_taxnumber': '12345678901', 'trans_paiddate': '2017-09-26 10:01:48', 'cus_cod': '123456', 'utm_source': 'utm_source', 'trans_status': '1',
 'cus_address_city': 'S\xc3\xa3o Paulo', 'aff_name': '', 'cus_email': 'cliente@teste.com', 'cus_address': 'Rua Teste', 'trans_value': '0.00', 'trans_paymentmethod': '0',
 'cus_address_number': '0', 'cus_address_comp': 'NI', 'cus_cel': '15-99999-9999'}>'''


    print resposta
    return dict()

def email_new_user():
    mail.send('acmorganti@outlook.com.br',
  'teste',
  'teste de envio de email')
