import re
import yaml
from datetime import date, datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.safestring import mark_safe

import markdown

from blog.models import BlogPost
from blog.tagging import ALLOWED_TAGS, normalize_and_validate_tags


class Command(BaseCommand):
    help = "Loads blog posts from local markdown files under blog_posts/."

    def handle(self, *args, **kwargs):
        posts_root = Path(settings.BASE_DIR) / "blog_posts"
        if not posts_root.exists():
            self.stdout.write(self.style.WARNING(f"No local blog_posts directory found at {posts_root}."))
            return

        md_files = sorted(posts_root.rglob("*.md"))
        if not md_files:
            self.stdout.write(self.style.WARNING(f"No markdown files found under {posts_root}."))
            return

        self.stdout.write(self.style.NOTICE(f"Processing {len(md_files)} markdown files from {posts_root}"))

        for md_file in md_files:
            relative_dir = md_file.parent.relative_to(settings.BASE_DIR)
            base_url = f"{settings.STATIC_URL.rstrip('/')}/{relative_dir.as_posix()}"
            self.process_markdown_file(md_file, base_url)

    def process_markdown_file(self, md_file: Path, base_url: str):
        content = md_file.read_text(encoding="utf-8")
        metadata, content = self.parse_markdown(content)
        if not metadata.get("title"):
            self.stdout.write(self.style.WARNING(f"Skipping '{md_file}': missing required 'title' in front matter."))
            return

        # Replace local image paths with URLs served from STATIC_URL
        content = self.replace_image_paths(content, base_url)

        extensions = [
            "markdown.extensions.fenced_code",
            "markdown.extensions.tables",
            "markdown.extensions.toc",
            "markdown.extensions.codehilite",
            "markdown.extensions.sane_lists",
            "markdown.extensions.extra",
        ]

        md = markdown.Markdown(extensions=extensions, extension_configs={})
        content = mark_safe(md.convert(content))

        normalised_tags, invalid_tags = normalize_and_validate_tags(metadata.get("tags"))
        if invalid_tags:
            source = md_file.as_posix()
            self.stdout.write(
                self.style.WARNING(
                    f"Ignoring disallowed tag(s) {invalid_tags} in '{source}'. "
                    f"Allowed tags: {', '.join(ALLOWED_TAGS)}"
                )
            )

        thumbnail_url = self.get_file_url(base_url, metadata.get("thumbnail", ""))
        defaults = {
            "description": metadata.get("description", ""),
            "content": content,
            "thumbnail": thumbnail_url,
            "post_name": md_file.stem,
            "tags": normalised_tags,
        }

        post_date = self.parse_post_date(metadata.get("date"))
        if post_date:
            defaults["date_posted"] = post_date

        BlogPost.objects.update_or_create(
            title=metadata["title"],
            defaults=defaults,
        )

    def parse_markdown(self, content):
        if content.startswith("---"):
            parts = content.split("---", 2)
            metadata = yaml.safe_load(parts[1])
            content = parts[2]
        else:
            metadata = {}
        return metadata, content

    def replace_image_paths(self, content, base_url):
        pattern = r"!\[([^\]]*)\]\(([^)]+)\)"

        def replace(match):
            alt_text, img_path = match.groups()
            img_url = self.get_file_url(base_url, img_path)
            return f"![{alt_text}]({img_url})"

        return re.sub(pattern, replace, content)

    def get_file_url(self, base_url, filename):
        filename = str(filename).strip()
        if filename:
            return f"{base_url}/{filename}"
        return ""

    def parse_post_date(self, raw_date):
        if not raw_date:
            return None

        if isinstance(raw_date, datetime):
            candidate = raw_date
        elif isinstance(raw_date, date):
            candidate = datetime.combine(raw_date, datetime.min.time())
        else:
            raw_value = str(raw_date).strip()
            try:
                candidate = datetime.fromisoformat(raw_value)
            except ValueError:
                try:
                    candidate = datetime.strptime(raw_value, "%Y-%m-%d")
                except ValueError:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Unable to parse date '{raw_value}'. Expected ISO 8601 or YYYY-MM-DD format."
                        )
                    )
                    return None

        if timezone.is_naive(candidate):
            candidate = timezone.make_aware(candidate)

        return candidate
