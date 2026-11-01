from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Post, Category, Comment

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/<string:slug>')
def post_detail(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()

    # Draft visibility security rule:
    # Drafts are strictly private to the author only!
    if not post.is_published:
        if not current_user.is_authenticated or current_user.id != post.user_id:
            abort(404)

    # Increment view count
    post.views_count += 1
    db.session.commit()

    # Related posts from the same category
    related_posts = []
    if post.category_id:
        related_posts = Post.query.filter(
            Post.category_id == post.category_id,
            Post.id != post.id,
            Post.is_published == True
        ).order_by(Post.created_at.desc()).limit(3).all()

    return render_template('blog/post_detail.html', post=post, related_posts=related_posts)


@blog_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    categories = Category.query.order_by(Category.name.asc()).all()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        summary = request.form.get('summary', '').strip()
        content = request.form.get('content', '').strip()
        category_id = request.form.get('category_id', type=int)
        cover_image = request.form.get('cover_image', '').strip()
        action = request.form.get('action', 'publish') # 'publish' or 'draft'

        if not title or not content:
            flash('Post title and content are required.', 'danger')
            return render_template('blog/create_post.html', categories=categories)

        is_published = (action == 'publish')
        slug = Post.generate_slug(title)

        post = Post(
            title=title,
            slug=slug,
            summary=summary,
            content=content,
            cover_image=cover_image if cover_image else None,
            category_id=category_id if category_id else None,
            is_published=is_published,
            author=current_user
        )

        db.session.add(post)
        db.session.commit()

        if is_published:
            flash('Your blog post has been published successfully!', 'success')
            return redirect(url_for('blog.post_detail', slug=post.slug))
        else:
            flash('Your post has been saved as a draft.', 'info')
            return redirect(url_for('dashboard.index', tab='drafts'))

    return render_template('blog/create_post.html', categories=categories)


@blog_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Authorization security: users can only edit their own posts
    if post.author != current_user:
        flash('You are not authorized to edit this post.', 'danger')
        abort(403)

    categories = Category.query.order_by(Category.name.asc()).all()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        summary = request.form.get('summary', '').strip()
        content = request.form.get('content', '').strip()
        category_id = request.form.get('category_id', type=int)
        cover_image = request.form.get('cover_image', '').strip()
        action = request.form.get('action', 'publish')

        if not title or not content:
            flash('Post title and content are required.', 'danger')
            return render_template('blog/edit_post.html', post=post, categories=categories)

        post.title = title
        post.summary = summary
        post.content = content
        post.category_id = category_id if category_id else None
        post.cover_image = cover_image if cover_image else None
        post.is_published = (action == 'publish')

        db.session.commit()

        if post.is_published:
            flash('Post updated and published successfully!', 'success')
            return redirect(url_for('blog.post_detail', slug=post.slug))
        else:
            flash('Post updated and saved as draft.', 'info')
            return redirect(url_for('dashboard.index', tab='drafts'))

    return render_template('blog/edit_post.html', post=post, categories=categories)


@blog_bp.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Authorization security: users can only delete their own posts
    if post.author != current_user:
        flash('You are not authorized to delete this post.', 'danger')
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Blog post was deleted successfully.', 'success')
    return redirect(url_for('dashboard.index'))


@blog_bp.route('/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)

    if not post.is_published and post.author != current_user:
        abort(404)

    content = request.form.get('content', '').strip()
    if not content:
        flash('Comment cannot be empty.', 'warning')
        return redirect(url_for('blog.post_detail', slug=post.slug) + '#comments')

    comment = Comment(
        content=content,
        post=post,
        author=current_user
    )
    db.session.add(comment)
    db.session.commit()

    flash('Comment posted successfully!', 'success')
    return redirect(url_for('blog.post_detail', slug=post.slug) + '#comments')


@blog_bp.route('/comment/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_slug = comment.post.slug

    # Comment can only be deleted by the comment author OR the post author
    if comment.author != current_user and comment.post.author != current_user:
        flash('You are not authorized to delete this comment.', 'danger')
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    flash('Comment removed.', 'info')
    return redirect(url_for('blog.post_detail', slug=post_slug) + '#comments')
