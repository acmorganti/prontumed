import datetime


db.define_table(
    'post_pub',
    Field('auth_id','reference auth_user'),
    Field('title','string',length=200,label="Título",default=None),
    Field('keyword','string',length=200,label='Meta Keyword',default=None),
    Field('description','string',length=200,label='Meta Description',default=None),
    Field('author','string',length=200,label='Autor',default=None),
    Field('dt_pub','date',label='Data Publicação',
            default=datetime.date.today()),
    Field('post','text',label='Post',default=None, ),
    auth.signature,
)

db.define_table(
    'comment_pub',
    Field('auth_id','reference auth_user'),
    Field('comment_pub','text',label='Comentário',default=''),
    Field('dt_com','date',label='Data',default=datetime.date.today()),
    auth.signature,
)
