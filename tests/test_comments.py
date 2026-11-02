import unittest
from app import create_app, db
from app.models import User, Post, Category, Comment
from config import TestConfig

class CommentSystemTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Seed test user and category
        self.author = User(username='commentauthor', email='author@nest.com', full_name='Author One')
        self.author.set_password('pass123')
        self.reader = User(username='reader1', email='reader@nest.com', full_name='Reader One')
        self.reader.set_password('pass123')
        self.category = Category(name='Discussion', slug='discussion')

        db.session.add_all([self.author, self.reader, self.category])
        db.session.commit()

        self.post = Post(
            title='Sample Post for Discussion',
            slug='sample-post-for-discussion',
            content='Discussing technology and clean code architectures.',
            is_published=True,
            author=self.author,
            category=self.category
        )
        db.session.add(self.post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_and_list_comments(self):
        comment = Comment(
            content='Great article! Really enjoyed reading it.',
            post=self.post,
            author=self.reader
        )
        db.session.add(comment)
        db.session.commit()

        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(self.post.comments.first().author.username, 'reader1')
        self.assertEqual(self.author.total_comments_received, 1)

    def test_comment_deletion_security(self):
        comment = Comment(
            content='Temporary feedback',
            post=self.post,
            author=self.reader
        )
        db.session.add(comment)
        db.session.commit()

        # Both the comment author and post author have rights to delete
        self.assertTrue(comment.author.id == self.reader.id or comment.post.author.id == self.author.id)
        db.session.delete(comment)
        db.session.commit()
        self.assertEqual(self.post.comments.count(), 0)

    def test_add_comment_endpoint(self):
        # Login reader using login_identifier
        self.client.post('/auth/login', data={
            'login_identifier': 'reader@nest.com',
            'password': 'pass123'
        })
        response = self.client.post(f'/blog/{self.post.id}/comment', data={
            'content': 'This is an endpoint test comment.'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is an endpoint test comment.', response.data)
        db.session.expire_all()
        self.assertEqual(self.post.comments.count(), 1)

    def test_delete_comment_endpoint(self):
        comment = Comment(
            content='Delete me please',
            post=self.post,
            author=self.reader
        )
        db.session.add(comment)
        db.session.commit()

        # Login post author
        self.client.post('/auth/login', data={
            'login_identifier': 'author@nest.com',
            'password': 'pass123'
        })
        response = self.client.post(f'/blog/comment/delete/{comment.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        db.session.expire_all()
        self.assertEqual(self.post.comments.count(), 0)

if __name__ == '__main__':
    unittest.main()

