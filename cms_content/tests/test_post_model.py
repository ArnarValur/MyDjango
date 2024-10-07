import logging

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from cms_content.models import Post

logger = logging.getLogger(__name__)


class PostModelTests(TestCase):

    #Set up the test environment (fake user)
    def setUp(self):
        self.author = User.objects.create_user(username='testuser', password='12345')

    #Test post creation saves correctly
    def test_post_creation_saves_correctly(self):
        logger.debug("Starting test_post_creation_saves_correctly")
        post = Post.objects.create(title="Test Post", content="Test Content", author=self.author)
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "Test Content")
        self.assertEqual(post.author, self.author)
        logger.debug("Finished test_post_creation_saves_correctly")

    #Test post creation with empty title
    def test_post_creation_with_empty_title(self):
        logger.debug("Starting test_post_creation_with_empty_title")
        post = Post(title="", content="Test Content", author=self.author)
        with self.assertRaises(ValidationError):
            post.full_clean()  # This will trigger the validation
            post.save()
        logger.debug("Finished test_post_creation_with_empty_title")

    #Test post creation with empty content
    def test_post_creation_with_empty_content(self):
        logger.debug("Starting test_post_creation_with_empty_content")
        post = Post.objects.create(title="Test Post", content="", author=self.author)
        self.assertEqual(post.content, "")
        logger.debug("Finished test_post_creation_with_empty_content")

    #Test post retrieval by id
    def test_post_retrieval_by_id(self):
        logger.debug("Starting test_post_retrieval_by_id")
        post = Post.objects.create(title="Test Post", content="Test Content", author=self.author)
        retrieved_post = Post.objects.get(id=post.id)
        self.assertEqual(retrieved_post, post)
        logger.debug("Finished test_post_retrieval_by_id")

    #Test post update saves correctly
    def test_post_update_saves_correctly(self):
        logger.debug("Starting test_post_update_saves_correctly")
        post = Post.objects.create(title="Test Post", content="Test Content", author=self.author)
        post.title = "Updated Post"
        post.save()
        updated_post = Post.objects.get(id=post.id)
        self.assertEqual(updated_post.title, "Updated Post")
        logger.debug("Finished test_post_update_saves_correctly")

    #Test post deletion
    def test_post_deletion_removes_post(self):
        logger.debug("Starting test_post_deletion_removes_post")
        post = Post.objects.create(title="Test Post", content="Test Content", author=self.author)
        post_id = post.id
        post.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post_id)
        logger.debug("Finished test_post_deletion_removes_post")

    #Test slug generation
    def test_slug_generation(self):
        logger.debug("Starting test_slug_generation")
        post = Post.objects.create(title="Test Post", content="Test Content", author=self.author)
        self.assertEqual(post.slug, 'test-post')
        logger.debug("Finished test_slug_generation")

    #Test that the slug is unique
    def test_unique_slug(self):
        logger.debug("Starting test_unique_slug")
        post = Post.objects.create(title="Test Post 1", content="Test Content", author=self.author)
        post2 = Post.objects.create(title="Test Post 2", content="Test Content", author=self.author)
        self.assertNotEqual(post.slug, post2.slug)
        logger.debug("Finished test_unique_slug")

    #Test post status
    def test_post_status(self):
        logger.debug("Starting test_post_status")
        post = Post.objects.create(title="Test Post", content="Test Content", author=self.author)
        self.assertEqual(post.status, 'draft')
        logger.debug("Finished test_post_status")

    #Test post views
    def test_post_views(self):
        logger.debug("Starting test_post_views")
        post = Post.objects.create(title="Test Post", content="Test Content", author=self.author)
        initial_views = post.views
        post.views += 1
        post.save()
        self.assertEqual(post.views, initial_views + 1)
        logger.debug("Finished test_post_views")

    #Test metadata fields
    def test_metadata_fields(self):
        logger.debug("Starting test_metadata_fields")
        post = Post.objects.create(title="Test Post", content="Test Content", author=self.author,
                                   meta_title="Meta Title", meta_description="Meta Description", meta_keywords="Meta Keywords")
        self.assertEqual(post.meta_title, "Meta Title")
        self.assertEqual(post.meta_description, "Meta Description")
        self.assertEqual(post.meta_keywords, "Meta Keywords")
        logger.debug("Finished test_metadata_fields")
