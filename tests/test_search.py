import unittest
from app import create_app, db
from app.models import User, Post, Category
from config import TestConfig

class SearchAndFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Seed test user
        self.user = User(username='searcher', email='searcher@nest.com', full_name='Search Tester')
        self.user.set_password('pass123')

        # Seed categories
        self.cat_tech = Category(name='Technology', slug='technology')
        self.cat_design = Category(name='Design', slug='design')

        db.session.add_all([self.user, self.cat_tech, self.cat_design])
        db.session.commit()

        # Seed posts
        self.post_tech = Post(
            title='Understanding Flask Application Architecture',
            slug='flask-architecture',
            summary='Deep dive into application factories and blueprints.',
            content='Full guide to clean code and patterns in Python web frameworks.',
            is_published=True,
            views_count=100,
            author=self.user,
            category=self.cat_tech
        )
        self.post_design = Post(
            title='Modern Glassmorphism UI Trends',
            slug='glassmorphism-trends',
            summary='Crafting aesthetic user interfaces with modern CSS.',
            content='Learn about backdrop-filters, subtle gradients, and typography.',
            is_published=True,
            views_count=250,
            author=self.user,
            category=self.cat_design
        )
        self.draft_post = Post(
            title='Secret Unpublished Draft Post on Flask',
            slug='secret-draft',
            summary='This is confidential and in draft state.',
            content='Secret technical information.',
            is_published=False,
            views_count=0,
            author=self.user,
            category=self.cat_tech
        )

        db.session.add_all([self.post_tech, self.post_design, self.draft_post])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_search_by_title(self):
        response = self.client.get('/explore?q=Flask')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Understanding Flask Application Architecture', response.data)
        # Verify drafts are NEVER leaked in public search
        self.assertNotIn(b'Secret Unpublished Draft Post', response.data)

    def test_search_by_content(self):
        response = self.client.get('/explore?q=typography')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Modern Glassmorphism UI Trends', response.data)
        self.assertNotIn(b'Understanding Flask Application Architecture', response.data)

    def test_filter_by_category(self):
        # Technology category
        response = self.client.get('/explore?category=technology')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Understanding Flask Application Architecture', response.data)
        self.assertNotIn(b'Modern Glassmorphism UI Trends', response.data)

        # Design category
        response_design = self.client.get('/explore?category=design')
        self.assertEqual(response_design.status_code, 200)
        self.assertIn(b'Modern Glassmorphism UI Trends', response_design.data)
        self.assertNotIn(b'Understanding Flask Application Architecture', response_design.data)

    def test_sort_by_views(self):
        response = self.client.get('/explore?sort=views')
        self.assertEqual(response.status_code, 200)
        # Most viewed (Design with 250 views) should appear before Tech (100 views)
        design_pos = response.data.find(b'Modern Glassmorphism UI Trends')
        tech_pos = response.data.find(b'Understanding Flask Application Architecture')
        self.assertTrue(design_pos != -1 and tech_pos != -1)
        self.assertTrue(design_pos < tech_pos)

    def test_empty_search_results(self):
        response = self.client.get('/explore?q=NonExistentKeywordXYZ')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No stories found', response.data)

if __name__ == '__main__':
    unittest.main()
