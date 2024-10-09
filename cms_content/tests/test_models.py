import uuid
import logging

from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.test import TestCase
from django.utils.text import slugify
from cms_content.models import Page, Link, update_page_from_link

logger = logging.getLogger(__name__)


def create_page(title="Test Page"):
    return Page.objects.create(title=title)


def create_link(label="Test Link", page=None):
    return Link.objects.create(label=label, page=page)


class ModelTest(TestCase):
    def test_link_is_created_with_page(self):
        logger.debug("Starting link_is_created_with_page")
        page = create_page()
        link = Link.objects.get(page=page)
        self.assertEqual(link.label, page.title)
        self.assertEqual(link.slug, page.slug)
        self.assertEqual(link.location, page.page_link_location)
        self.assertEqual(link.status, page.page_status)
        self.assertEqual(link.order, page.order)
        logger.debug("Finished link_is_created_with_page")

    def test_page_updates_link_on_save(self):
        logger.debug("Starting page_updates_link_on_save")

        post_save.disconnect(update_page_from_link, sender=Link)

        page = create_page()
        page.title = "Updated Title"
        page.save()
        link = Link.objects.get(page=page)
        self.assertEqual(link.label, "Updated Title")
        self.assertEqual(link.slug, slugify("Updated Title"))
        logger.debug("Finished page_updates_link_on_save")

        post_save.connect(update_page_from_link, sender=Link)

    def test_link_updates_page_on_save(self):
        logger.debug("Starting link_updates_page_on_save")
        page = create_page()
        link = Link.objects.get(page=page)
        link.label = "Updated Label"
        link.save()
        page.refresh_from_db()
        self.assertEqual(page.title, "Updated Label")
        self.assertEqual(page.slug, slugify("Updated Label"))
        logger.debug("Finished link_updates_page_on_save")

    def test_link_deletion_does_not_delete_page(self):
        logger.debug("Starting link_deletion_does_not_delete_page")
        page = create_page()
        link = Link.objects.get(page=page)
        link.delete()
        self.assertTrue(Page.objects.filter(id=page.id).exists())
        logger.debug("Finished link_deletion_does_not_delete_page")

    def test_page_deletion_deletes_link(self):
        logger.debug("Starting page_deletion_deletes_link")
        page = create_page()
        page_id = page.id
        page.delete()
        self.assertFalse(Link.objects.filter(page_id=page_id).exists())
        logger.debug("Finished page_deletion_deletes_link")
