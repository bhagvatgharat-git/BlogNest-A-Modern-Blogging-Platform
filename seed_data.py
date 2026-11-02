"""
BlogNest Database Seeder Script
Populates the database with realistic sample authors, categories,
published stories, drafts, and community discussion comments.
"""
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Post, Category, Comment

def seed_database():
    app = create_app()
    with app.app_context():
        print("[SEED] Seeding BlogNest Database...")

        # Reset / Ensure tables
        db.create_all()

        # Check if users already exist
        if User.query.first():
            print("Database already contains data. Clearing existing records for clean seed...")
            Comment.query.delete()
            Post.query.delete()
            Category.query.delete()
            User.query.delete()
            db.session.commit()

        # 1. Create Sample Users
        user1 = User(
            username='bhagvat',
            email='bhagvat@blognest.dev',
            full_name='Bhagvat Gharat',
            bio='Software engineer, open-source enthusiast, and creator of BlogNest. Writing on Flask, cloud architecture, and modern web design.',
            avatar_url='https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
        )
        user1.set_password('Admin123!')

        user2 = User(
            username='sarah_ux',
            email='sarah@blognest.dev',
            full_name='Sarah Jenkins',
            bio='Product designer and design system architect. Passionate about glassmorphism, micro-interactions, and visual harmony.',
            avatar_url='https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=200&q=80'
        )
        user2.set_password('Designer123!')

        user3 = User(
            username='alex_cloud',
            email='alex@blognest.dev',
            full_name='Alex Chen',
            bio='Distributed systems architect. Obsessed with scalable APIs, database performance tuning, and developer tooling.',
            avatar_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80'
        )
        user3.set_password('Cloud123!')

        db.session.add_all([user1, user2, user3])
        db.session.commit()
        print("  [OK] Created 3 sample authors")

        # 2. Create Categories
        cat_web = Category(
            name='Web Development',
            slug='web-development',
            description='Modern frontend and backend engineering, frameworks, and architecture.',
            color_code='#0284c7'
        )
        cat_ai = Category(
            name='AI & Machine Learning',
            slug='ai-and-ml',
            description='LLMs, neural networks, predictive models, and modern AI engineering.',
            color_code='#0ea5e9'
        )
        cat_design = Category(
            name='UI/UX Design',
            slug='ui-ux-design',
            description='Aesthetics, user interface design systems, typography, and responsive layouts.',
            color_code='#38bdf8'
        )
        cat_arch = Category(
            name='Clean Architecture',
            slug='clean-architecture',
            description='Best practices, design patterns, testing methodologies, and refactoring.',
            color_code='#0369a1'
        )
        cat_career = Category(
            name='Productivity & Career',
            slug='productivity-and-career',
            description='Tips, workflows, developer mindset, and career growth strategies.',
            color_code='#075985'
        )

        db.session.add_all([cat_web, cat_ai, cat_design, cat_arch, cat_career])
        db.session.commit()
        print("  [OK] Created 5 topics/categories")

        # 3. Create Published Posts
        post1 = Post(
            title='Building Enterprise-Ready Python Flask Applications in 2026',
            slug='building-enterprise-ready-flask-applications-2026',
            summary='Discover how application factories, blueprints, and clean architectural boundaries turn Flask into a heavyweight enterprise engine.',
            content="""Flask is often stereotyped as a minimal microframework only suitable for quick prototypes or toy APIs. However, when combined with clean software engineering patterns, Flask offers unparalleled developer flexibility and blazing fast performance.

In this deep dive, we explore how to organize real-world production Flask applications:

1. The Application Factory Pattern
Instead of declaring a global app instance, instantiate your Flask application inside a factory function `create_app()`. This prevents cyclical imports, simplifies unit testing with in-memory SQLite fixtures, and makes multi-environment configuration seamless.

2. Modular Architecture with Blueprints
Break down your route handlers into modular blueprints: Auth, Blog, Dashboard, and Main. Each blueprint manages its own URL prefixes, templates, and domain concerns.

3. Robust Data Persistence with SQLAlchemy ORM
Use explicit database models with relationships, cascades, and indexes on frequently queried fields like `slug`, `username`, and `created_at`.

Embracing these design principles empowers engineering teams to deliver clean, maintainable, and high-velocity web software.""",
            cover_image='https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80',
            is_published=True,
            views_count=342,
            created_at=datetime.utcnow() - timedelta(days=5),
            author=user1,
            category=cat_web
        )

        post2 = Post(
            title='The Art of Light Blue & Glassmorphism: Designing Modern Web UIs',
            slug='art-of-light-blue-glassmorphism-web-design',
            summary='A practical guide to implementing airy, radiant user interfaces with backdrop filters, subtle border highlights, and refined typography.',
            content="""Great digital design is invisible; it gets out of the user's way while evoking an emotional sense of clarity and delight.

The Light Blue and White color system has emerged as a favorite among modern developer platforms and productivity tools. Unlike heavy dark modes or sterile high-contrast whites, a light blue palette provides:

- Reduced Visual Fatigue: Soft sky-blue hues and subtle gradient backdrops soothe the eyes during long reading sessions.
- Spatial Depth: Using `backdrop-filter: blur(12px)` paired with translucent white panels (`rgba(255, 255, 255, 0.88)`) creates realistic floating elevations.
- Micro-interactions: Elevating cards slightly on hover (`translateY(-4px)`) coupled with soft tinted shadows (`rgba(14, 165, 233, 0.12)`) rewards user interaction.

When typography is set with modern geometric sans fonts like Plus Jakarta Sans, readability scales effortlessly across both desktop monitors and mobile touchscreens.""",
            cover_image='https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=1200&q=80',
            is_published=True,
            views_count=518,
            created_at=datetime.utcnow() - timedelta(days=3),
            author=user2,
            category=cat_design
        )

        post3 = Post(
            title='Understanding Autonomous AI Agents and LLM Workflows',
            slug='understanding-autonomous-ai-agents-llm-workflows',
            summary='How modern autonomous coding agents reason, call tools, inspect state, and pair-program alongside software developers.',
            content="""The landscape of software development has entered an inflection point with autonomous coding agents. Rather than simple code completions, autonomous agents can plan multi-step workflows, inspect project file trees, execute terminal commands, and verify test suites.

Key pillars of agentic AI systems:

1. Grounding in Real Workspace Context
Agents do not work in a vacuum; they analyze active documents, git commit logs, and directory structures to understand existing coding conventions.

2. Autonomous Verification Loops
Writing code is only half the battle. High-grade agents execute unit tests, capture errors, and iteratively refine their solutions until all test assertions pass.

3. Pair-Programming Alignment
Through clear markdown artifacts, status summaries, and interactive feedback, agents and human engineers collaborate as high-performing co-pilots.""",
            cover_image='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80',
            is_published=True,
            views_count=420,
            created_at=datetime.utcnow() - timedelta(days=2),
            author=user1,
            category=cat_ai
        )

        post4 = Post(
            title='Zero-Downtime SQLite Optimizations for Web Applications',
            slug='zero-downtime-sqlite-optimizations',
            summary='Why SQLite is capable of handling millions of requests per day and how WAL mode unlocks high-concurrency read performance.',
            content="""SQLite is the most widely deployed database engine on Earth, yet developers often underestimate its sheer power for modern full-stack web applications.

By enabling Write-Ahead Logging (WAL mode), SQLite decouples readers from writers:
- Readers never block writers.
- Writers never block readers.
- Concurrency scales beautifully on modern NVMe drives.

When combined with SQLAlchemy connection pooling, sensible composite indexing on search columns, and proper database transaction scoping, SQLite delivers microsecond query latencies with zero operational complexity.""",
            cover_image='https://images.unsplash.com/photo-1544383835-bda2bc66a55d?auto=format&fit=crop&w=1200&q=80',
            is_published=True,
            views_count=215,
            created_at=datetime.utcnow() - timedelta(days=1),
            author=user3,
            category=cat_arch
        )

        post5 = Post(
            title='Mastering Developer Productivity: Focus Blocks and Deep Work',
            slug='mastering-developer-productivity-deep-work',
            summary='Practical habits to eliminate context switching and maintain long uninterrupted stretches of cognitive flow.',
            content="""In software engineering, continuous distraction is the enemy of architecture. Building complex systems requires holding deep mental models of data flow in working memory.

Here are three habits that dramatically boost engineering output:

1. Time-Blocked Deep Work Sprints
Schedule 90-minute blocks where all notification badges, chat apps, and email tabs are closed.

2. Documenting Decisions in Git Commits
Write atomic commits with meaningful descriptions. Your future self and team members will understand the 'why' behind architectural choices.

3. Testing as You Go
Automated tests eliminate fear. When you have a solid test suite, refactoring is joyful rather than stressful.""",
            cover_image='https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80',
            is_published=True,
            views_count=189,
            created_at=datetime.utcnow() - timedelta(hours=8),
            author=user2,
            category=cat_career
        )

        # 4. Create Draft Post (For demonstrating author draft isolation)
        draft1 = Post(
            title='[Confidential Draft] Future Roadmap for BlogNest v2.0',
            slug='confidential-draft-future-roadmap-v2',
            summary='Early brainstorming notes for upcoming features and integrations.',
            content='This is a private author draft. It is strictly visible only to Bhagvat in his dashboard and cannot be accessed by other users.',
            cover_image=None,
            is_published=False,
            views_count=0,
            created_at=datetime.utcnow(),
            author=user1,
            category=cat_web
        )

        db.session.add_all([post1, post2, post3, post4, post5, draft1])
        db.session.commit()
        print("  [OK] Created 5 published stories and 1 private author draft")

        # 5. Create Community Comments
        c1 = Comment(
            content='Exceptional breakdown of Flask application architecture! The application factory pattern completely solved circular import issues in my team.',
            created_at=datetime.utcnow() - timedelta(days=4),
            author=user2,
            post=post1
        )
        c2 = Comment(
            content='Great writeup! Pairing Flask with SQLite in WAL mode gives incredible sub-millisecond query responses for read-heavy portals.',
            created_at=datetime.utcnow() - timedelta(days=3),
            author=user3,
            post=post1
        )
        c3 = Comment(
            content='Thank you for reading and leaving feedback! Glad this architectural structure proved helpful.',
            created_at=datetime.utcnow() - timedelta(days=2),
            author=user1,
            post=post1
        )
        c4 = Comment(
            content='The Light Blue and White theme on BlogNest looks stunning and crisp. The typography choices really make long articles a pleasure to read.',
            created_at=datetime.utcnow() - timedelta(days=1),
            author=user1,
            post=post2
        )
        c5 = Comment(
            content='The point on autonomous verification loops is spot on. Continuous automated testing turns agents from toys into real engineering partners.',
            created_at=datetime.utcnow() - timedelta(hours=12),
            author=user2,
            post=post3
        )

        db.session.add_all([c1, c2, c3, c4, c5])
        db.session.commit()
        print("  [OK] Created 5 community discussion comments")

        print("\n=== Database Seeding Complete! ===")
        print("Sample Login Credentials:")
        print("  1. Username: bhagvat     | Password: Admin123!")
        print("  2. Username: sarah_ux    | Password: Designer123!")
        print("  3. Username: alex_cloud  | Password: Cloud123!")
        print("==================================")

if __name__ == '__main__':
    seed_database()
