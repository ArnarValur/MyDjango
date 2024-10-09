import uuid
import logging

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.text import slugify
from cms_content.models import Page, Link

logger = logging.getLogger(__name__)

class LinkModelTests(TestCase):
    def create_page(self, title="Test Page"):
        return Page.objects.create(title=title)

    def create_link(self, label="Test Link", page=None):
        return Link.objects.create(label=label, page=page)

    def test_link_saves_with_slug(self):
        logger.debug("Starting link_saves_with_slug")
        link = self.create_link()
        self.assertEqual(link.slug, slugify(link.label))
        logger.debug("Finished link_saves_with_slug")

    def test_link_saves_with_unique_slug(self):
        logger.debug("Starting link_saves_with_unique_slug")
        link1 = self.create_link()
        link2 = self.create_link()
        self.assertNotEqual(link1.slug, link2.slug)
        logger.debug("Finished link_saves_with_unique_slug")

    def test_link_creation_with_duplicate_label_raises_error(self):
        logger.debug("Starting link_creation_with_duplicate_label_raises_error")
        self.create_link(label="Duplicate Label")
        with self.assertRaises(ValidationError):
            duplicate_link = Link(label="Duplicate Label")
            duplicate_link.full_clean()  # This will trigger the validation
            duplicate_link.save()
        logger.debug("Finished link_creation_with_duplicate_label_raises_error")

    def test_link_creation_with_long_label_raises_error(self):
        logger.debug("Starting link_creation_with_long_label_raises_error")
        long_label = "a" * 201  # Exceeds the max_length of 200
        link = Link(label=long_label)
        with self.assertRaises(ValidationError):
            link.full_clean()  # This will trigger the validation
            link.save()
        logger.debug("Finished link_creation_with_long_label_raises_error")

    def test_link_slug_generation_with_special_characters(self):
        logger.debug("Starting link_slug_generation_with_special_characters")
        link = self.create_link(label="Test Link!@#")
        self.assertEqual(link.slug, "test-link")
        logger.debug("Finished link_slug_generation_with_special_characters")

    def test_link_slug_generation_with_unicode_characters(self):
        logger.debug("Starting link_slug_generation_with_unicode_characters")
        link = self.create_link(label="Tést Lïnk")
        self.assertEqual(link.slug, "test-link")
        logger.debug("Finished link_slug_generation_with_unicode_characters")