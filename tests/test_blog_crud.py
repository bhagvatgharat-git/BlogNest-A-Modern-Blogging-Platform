import unittest
from app import create_app, db
from app.models import User, Post, Category
from config import TestConfig

class BlogCrudTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Seed author and competitor
        self.author = User(username='alexwriter', email='alex@nest.com', full_name='Alex Writer')
        self.author.set_password('pass123')
        self.other_user = User(username='bobhacker', email='bob@nest.com', full_name='Bob Hacker')
        self.other_user.set_password('pass123')

        self.category = Category(name='Engineering', slug='engineering')

        db.session.add_all([self.author, self.other_user, self.category])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_post_creation_and_slug_generation(self):
        # Login author
        self.client.post('/auth/login', data={
            'login_identifier': 'alexwriter',
            'password': 'pass123'
        })

        # Create published post
        response = self.client.post('/blog/create', data={
            'title': 'The Future of Web Development in 2026',
            'summary': 'Exploring new advancements in backend and fullstack engineering.',
            'content': 'Comprehensive writeup about clean architecture, speed, and tooling.' * 10,
            'category_id': self.category.id,
            'action': 'publish'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        post = Post.query.filter_by(title='The Future of Web Development in 2026').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.slug, 'the-future-of-web-development-in-2026')
        self.assertTrue(post.is_published)
        self.assertEqual(post.author.id, self.author.id)

    def test_draft_privacy_enforcement(self):
        # Create draft post
        draft = Post(
            title='Confidential Secret Draft',
            slug='confidential-secret-draft',
            summary='Draft summary',
            content='This is a secret unpublished post.',
            is_published=False,
            author=self.author,
            category=self.category
        )
        db.session.add(draft)
        db.session.commit()

        # Anonymous visitor tries to view draft -> 404
        anon_resp = self.client.get(f'/blog/{draft.slug}')
        self.assertEqual(anon_resp.status_code, 404)

        # Another authenticated user tries to view draft -> 404
        self.client.post('/auth/login', data={
            'login_identifier': 'bobhacker',
            'password': 'pass123'
        })
        bob_resp = self.client.get(f'/blog/{draft.slug}')
        self.assertEqual(bob_resp.status_code, 404)

        # Owner can view draft
        self.client.get('/auth/logout')
        self.client.post('/auth/login', data={
            'login_identifier': 'alexwriter',
            'password': 'pass123'
        })
        author_resp = self.client.get(f'/blog/{draft.slug}')
        self.assertEqual(author_resp.status_code, 200)
        self.assertIn(b'Private Draft', author_resp.data)

    def test_unauthorized_post_editing_prevented(self):
        post = Post(
            title='Alex Owns This Post',
            slug='alex-post',
            content='Only Alex should be allowed to edit.',
            is_published=True,
            author=self.author,
            category=self.category
        )
        db.session.add(post)
        db.session.commit()

        # Bob logs in and tries to edit Alex's post -> 403 Forbidden
        self.client.post('/auth/login', data={
            'login_identifier': 'bobhacker',
            'password': 'pass123'
        })
        resp = self.client.post(f'/blog/edit/{post.id}', data={
            'title': 'Hacked Title',
            'content': 'Hacked content'
        })
        self.assertEqual(resp.status_code, 403)
        db.session.expire_all()
        self.assertEqual(post.title, 'Alex Owns This Post')

    def test_unauthorized_post_deletion_prevented(self):
        post = Post(
            title='Alex Safe Post',
            slug='alex-safe-post',
            content='Cannot be deleted by strangers.',
            is_published=True,
            author=self.author,
            category=self.category
        )
        db.session.add(post)
        db.session.commit()

        # Bob logs in and tries to delete
        self.client.post('/auth/login', data={
            'login_identifier': 'bobhacker',
            'password': 'pass123'
        })
        resp = self.client.post(f'/blog/delete/{post.id}')
        self.assertEqual(resp.status_code, 403)
        self.assertIsNotNone(Post.query.get(post.id))

        # Alex logs in and successfully deletes
        self.client.get('/auth/logout')
        self.client.post('/auth/login', data={
            'login_identifier': 'alexwriter',
            'password': 'pass123'
        })
        delete_resp = self.client.post(f'/blog/delete/{post.id}', follow_redirects=True)
        self.assertEqual(delete_resp.status_code, 200)
        self.assertIsNone(Post.query.get(post.id))

if __name__ == '__main__':
    unittest.main()
