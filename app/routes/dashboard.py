from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Post

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    tab = request.args.get('tab', 'all')
    page = request.args.get('page', 1, type=int)

    base_query = Post.query.filter_by(user_id=current_user.id)

    if tab == 'published':
        posts_query = base_query.filter_by(is_published=True)
    elif tab == 'drafts':
        posts_query = base_query.filter_by(is_published=False)
    else:
        posts_query = base_query

    pagination = posts_query.order_by(Post.updated_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    stats = {
        'total_posts': current_user.posts.count(),
        'published_posts': current_user.published_posts_count,
        'draft_posts': current_user.drafts_count,
        'total_views': current_user.total_views,
        'comments_received': current_user.total_comments_received
    }

    return render_template(
        'dashboard/index.html',
        posts=pagination.items,
        pagination=pagination,
        stats=stats,
        current_tab=tab
    )
