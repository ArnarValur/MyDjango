import logging
from django.core.exceptions import ValidationError
from django.test import TestCase
from cms_content.models import Page

logger = logging.getLogger(__name__)


class PageModelTests(TestCase):
    def test_page_creation_saves_correctly(self):
        logger.debug("Starting test_page_creation_saves_correctly")
        page = Page.objects.create(title="Test Page", content="Test Content")
        self.assertEqual(page.title, "Test Page")
        self.assertEqual(page.content, "Test Content")
        logger.debug("Finished test_page_creation_saves_correctly")

    def test_page_creation_with_empty_title(self):
        logger.debug("Starting test_page_creation_with_empty_title")
        page = Page(title="", content="Test Content")
        with self.assertRaises(ValidationError):
            page.full_clean()  # This will trigger the validation
            page.save()
        logger.debug("Finished test_page_creation_with_empty_title")

    def test_page_creation_with_empty_content(self):
        logger.debug("Starting test_page_creation_with_empty_content")
        page = Page.objects.create(title="Test Page", content="")
        self.assertEqual(page.content, "")
        logger.debug("Finished test_page_creation_with_empty_content")

    def test_page_retrieval_by_id(self):
        logger.debug("Starting test_page_retrieval_by_id")
        page = Page.objects.create(title="Test Page", content="Test Content")
        retrieved_page = Page.objects.get(id=page.id)
        self.assertEqual(retrieved_page, page)
        logger.debug("Finished test_page_retrieval_by_id")

    def test_page_update_saves_correctly(self):
        logger.debug("Starting test_page_update_saves_correctly")
        page = Page.objects.create(title="Test Page", content="Test Content")
        page.title = "Updated Page"
        page.save()
        updated_page = Page.objects.get(id=page.id)
        self.assertEqual(updated_page.title, "Updated Page")
        logger.debug("Finished test_page_update_saves_correctly")

    def test_page_deletion_removes_page(self):
        logger.debug("Starting test_page_deletion_removes_page")
        page = Page.objects.create(title="Test Page", content="Test Content")
        page_id = page.id
        page.delete()
        with self.assertRaises(Page.DoesNotExist):
            Page.objects.get(id=page_id)
        logger.debug("Finished test_page_deletion_removes_page")
