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

    def test_page_creation_with_different_statuses(self):
        logger.debug("Starting page_creation_with_different_statuses")
        statuses = ['draft', 'published', 'private']
        for status in statuses:
            page = Page.objects.create(title=f"Test Page {status}", content="Test Content", page_status=status)
            self.assertEqual(page.page_status, status)
        logger.debug("Finished page_creation_with_different_statuses")

    def test_page_creation_with_different_link_locations(self):
        logger.debug("Starting page_creation_with_different_link_locations")
        locations = ['navbar', 'header', 'footer', 'sidebar', 'unsorted']
        for location in locations:
            page = Page.objects.create(title=f"Test Page {location}", content="Test Content", page_link_location=location)
            self.assertEqual(page.page_link_location, location)
        logger.debug("Finished page_creation_with_different_link_locations")

    def test_page_slug_generation_without_parent(self):
        logger.debug("Starting page_slug_generation_without_parent")
        page = Page.objects.create(title="Test Page", content="Test Content")
        self.assertEqual(page.slug, "test-page")
        logger.debug("Finished page_slug_generation_without_parent")

    def test_page_slug_generation_with_parent(self):
        logger.debug("Starting page_slug_generation_with_parent")
        parent_page = Page.objects.create(title="Parent Page", content="Parent Content")
        child_page = Page.objects.create(title="Child Page", content="Child Content", parent=parent_page)
        self.assertEqual(child_page.slug, "parent-page/child-page")
        logger.debug("Finished page_slug_generation_with_parent")

    def test_page_creation_with_duplicate_title_raises_error(self):
        Page.objects.create(title="Duplicate Title", content="Content 1")
        with self.assertRaises(ValidationError):
            duplicate_page = Page(title="Duplicate Title", content="Content 2")
            duplicate_page.full_clean()  # This will trigger the validation
            duplicate_page.save()

    def test_page_creation_with_long_title_raises_error(self):
        long_title = "a" * 201  # Exceeds the max_length of 200
        page = Page(title=long_title, content="Test Content")
        with self.assertRaises(ValidationError):
            page.full_clean()  # This will trigger the validation
            page.save()

    def test_page_creation_with_invalid_status_raises_error(self):
        page = Page(title="Test Page", content="Test Content", page_status="invalid_status")
        with self.assertRaises(ValidationError):
            page.full_clean()  # This will trigger the validation
            page.save()

    def test_page_creation_with_invalid_link_location_raises_error(self):
        page = Page(title="Test Page", content="Test Content", page_link_location="invalid_location")
        with self.assertRaises(ValidationError):
            page.full_clean()  # This will trigger the validation
            page.save()

    def test_page_slug_generation_with_special_characters(self):
        page = Page.objects.create(title="Test Page!@#", content="Test Content")
        self.assertEqual(page.slug, "test-page")

    def test_page_slug_generation_with_unicode_characters(self):
        page = Page.objects.create(title="Tést Päge", content="Test Content")
        self.assertEqual(page.slug, "test-page")