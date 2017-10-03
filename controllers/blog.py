def index():
    response.title += ' | Posts'
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
    total = db(db.post_pub).count()
    posts_per_page = 5
    pages = total / posts_per_page
    if total%pages:
        posts_per_page += 1
    start = (page-1)*posts_per_page
    end = page*posts_per_page
    posts = db(db.post_pub).select(db.post_pub.post,db.post_pub.id,db.post_pub.title,
                                  orderby=~db.post_pub.dt_pub,
                                  limitby=(start,end))
    return dict(posts = posts, page=page, pages = pages)

def read():
    post_id = request.args(0)
    post = db(db.post_pub.id == post_id).select().first().post
    return dict(post = post)

@auth.requires_login()
def new():
    form = SQLFORM(db.post_pub)
    form.vars.auth_id = auth.user.id
    if form.process().accepted:
        response.flash = 'Novo post criado!'
    elif form.errors:
        response.flash = 'Verifique os erros!'
    return dict(form = form)

@auth.requires_login()
def edit():
    post = db(db.post_pub.id == request.vars.post_id).select().first()
    form = SQLFORM(db.post_pub, post)
    form.vars.auth_id = auth.user.id
    if form.process().accepted:
        response.flash = 'Novo post criado!'
    elif form.errors:
        response.flash = 'Verifique os erros!'
    return dict(form = form)
