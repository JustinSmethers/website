from pathlib import Path
import subprocess
import sys

from django.core.exceptions import ValidationError
from django.test import TestCase

from blog.models import BlogPost
from blog.tagging import normalize_and_validate_tags


class TaggingUtilsTests(TestCase):
    def test_normalize_and_validate_tags_filters_invalid_entries(self):
        normalised, invalid = normalize_and_validate_tags(
            [" Post ", "TALK", "notes", "unknown", 123, "post"]
        )

        self.assertEqual(normalised, ["post", "talk", "notes"])
        self.assertEqual(invalid, ["unknown", "123"])


class BlogPostModelTests(TestCase):
    def test_tags_are_normalised_on_save(self):
        post = BlogPost.objects.create(
            title="Tagged Post",
            description="A post with tags",
            content="Body",
            thumbnail="https://example.com/image.png",
            post_name="tagged-post",
            tags=[" POST ", "talk"],
        )

        self.assertEqual(post.tags, ["post", "talk"])

    def test_invalid_tags_raise_validation_error(self):
        post = BlogPost(
            title="Bad Tags",
            description="Invalid tags should fail",
            content="Body",
            thumbnail="https://example.com/image.png",
            post_name="bad-tags",
            tags=["invalid"],
        )

        with self.assertRaises(ValidationError):
            post.save()


class TagValidationScriptTests(TestCase):
    def test_validate_tags_script_passes_for_repository_content(self):
        project_root = Path(__file__).resolve().parents[1]
        script_path = project_root / "scripts" / "validate_tags.py"
        result = subprocess.run(
            [sys.executable, str(script_path)], capture_output=True, text=True
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)


class HomePageTests(TestCase):
    def test_homepage_shows_the_blog(self):
        post = BlogPost.objects.create(
            title="A published post",
            post_name="published-post",
            tags=["post"],
        )

        response = self.client.get("/")

        self.assertTemplateUsed(response, "blog/blog_layout.html")
        self.assertContains(response, "<title>Justin Smethers | Senior Analytics Engineer</title>")
        self.assertContains(response, post.title)
        self.assertContains(response, 'href="/blog/post/published-post/"')

    def test_old_blog_index_serves_the_homepage_without_redirecting(self):
        root = self.client.get("/")
        old_blog = self.client.get("/blog/")

        self.assertContains(old_blog, '<link rel="canonical" href="https://justinsmethers.com/">')
        self.assertEqual(old_blog.content, root.content)
