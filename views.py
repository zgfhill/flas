@main.route('/', methods=['GET', 'POST'])
def index():
	show_followed = False
	if current_user.is_authenticated:
		show_followed = request.args.get('show_followed', '')
	if show_followed:
		query = current_user.followed_posts
	else:
		query = Post.query
	pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=20, error_out=False)
	posts = pagination.items
	return render_template('index.html', form=form, posts=posts, show_followed=show_followed, pagination=pagination)

@main.route('/all')
@login_required
def show_all():
	resp = make_response(redirect(url_for('.index')))
	resp.set_cookie('show_followed', '', max_age=30*24*60*60)
	return resp

@main.route('/following')
@login_required
def show_followed():
	resp = make_response(redirect(url_for('.index')))
	resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
	return resp
