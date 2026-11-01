from flask import Blueprint, render_template, request, current_app
from sqlalchemy import or_
from app.models import Post, Category, User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 6)

    # Base query: only published posts
    query = Post.query.filter_by(is_published=True)

    # Optional category filter on homepage
    category_slug = request.args.get('category')
    selected_category = None
    if category_slug:
        selected_category = Category.query.filter_by(slug=category_slug).first()
        if selected_category:
            query = query.filter_by(category_id=selected_category.id)

    # Optional quick search
    search_query = request.args.get('q', '').strip()
    if search_query:
        query = query.filter(
            or_(
                Post.title.ilike(f'%{search_query}%'),
                Post.summary.ilike(f'%{search_query}%'),
                Post.content.ilike(f'%{search_query}%')
            )
        )

    pagination = query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    posts = pagination.items

    # Featured post (e.g. highest view count among published posts)
    featured_post = Post.query.filter_by(is_published=True).order_by(Post.views_count.desc(), Post.created_at.desc()).first()

    # Community stats
    total_posts = Post.query.filter_by(is_published=True).count()
    total_authors = User.query.count()
    total_categories = Category.query.count()

    return render_template(
        'main/index.html',
        posts=posts,
        pagination=pagination,
        featured_post=featured_post,
        selected_category=selected_category,
        search_query=search_query,
        stats={
            'total_posts': total_posts,
            'total_authors': total_authors,
            'total_categories': total_categories
        }
    )


@main_bp.route('/explore')
def explore():
    page = request.args.get('page', 1, type=int)
    category_slug = request.args.get('category', '').strip()
    search_query = request.args.get('q', '').strip()
    sort_by = request.args.get('sort', 'latest')

    query = Post.query.filter_by(is_published=True)

    selected_category = None
    if category_slug:
        selected_category = Category.query.filter_by(slug=category_slug).first()
        if selected_category:
            query = query.filter_by(category_id=selected_category.id)

    if search_query:
        query = query.filter(
            or_(
                Post.title.ilike(f'%{search_query}%'),
                Post.summary.ilike(f'%{search_query}%'),
                Post.content.ilike(f'%{search_query}%')
            )
        )

    # Sorting options
    if sort_by == 'views':
        query = query.order_by(Post.views_count.desc(), Post.created_at.desc())
    elif sort_by == 'oldest':
        query = query.order_by(Post.created_at.asc())
    else: # latest
        query = query.order_by(Post.created_at.desc())

    pagination = query.paginate(page=page, per_page=9, error_out=False)

    return render_template(
        'main/explore.html',
        posts=pagination.items,
        pagination=pagination,
        selected_category=selected_category,
        search_query=search_query,
        sort_by=sort_by
    )


@main_bp.route('/author/<string:username>')
def author_profile(username):
    author = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)

    # Strictly only published posts visible to public
    pagination = author.posts.filter_by(is_published=True).order_by(
        Post.created_at.desc()
    ).paginate(page=page, per_page=6, error_out=False)

    return render_template(
        'main/author.html',
        author=author,
        posts=pagination.items,
        pagination=pagination
    )


@main_bp.route('/about')
def about():
    return render_template('main/about.html')
