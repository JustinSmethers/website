"""Render the existing Django blog as a static site without production access."""

import os
from pathlib import Path
import shutil
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def main() -> None:
    # Always use the isolated settings, even if the shell targets production.
    os.environ["DJANGO_SETTINGS_MODULE"] = "buzzz.build_settings"
    import django

    django.setup()

    from django.core.management import call_command
    from django.test import Client, override_settings
    from django.urls import reverse

    from blog.models import BlogPost

    call_command("migrate", verbosity=0, interactive=False)
    call_command("load_local_posts")
    posts = list(BlogPost.objects.order_by("post_name"))
    expected_posts = list((PROJECT_ROOT / "blog_posts").rglob("*.md"))
    if not posts or len(posts) != len(expected_posts):
        raise RuntimeError("Every Markdown post must produce one published page.")

    output = PROJECT_ROOT / "dist"
    with tempfile.TemporaryDirectory(prefix="static-build-", dir=PROJECT_ROOT) as temporary:
        staged = Path(temporary)
        with override_settings(STATIC_ROOT=staged / "static"):
            call_command("collectstatic", verbosity=0, interactive=False, ignore=["*.md", "admin"])

        client = Client()
        paths = [reverse("blog:index")]
        paths.extend(reverse("blog:blog_detail", args=[post.post_name]) for post in posts)
        for path in paths:
            response = client.get(path)
            if response.status_code != 200:
                raise RuntimeError(f"Unable to render {path}: HTTP {response.status_code}")
            page = staged / path.lstrip("/") / "index.html"
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_bytes(response.content)

        redirects = ["/ /blog/ 301"]
        # The original GitHub importer used strip('.md'), which also removed
        # leading/trailing m and d characters from three published URLs.
        # Keep externally shared links working after using proper file stems.
        for source in sorted(expected_posts):
            legacy_name = source.name.strip(".md")
            if legacy_name != source.stem:
                canonical = reverse("blog:blog_detail", args=[source.stem])
                legacy = reverse("blog:blog_detail", args=[legacy_name])
                redirects.append(f"{legacy} {canonical} 301")
        (staged / "_redirects").write_text("\n".join(redirects) + "\n", encoding="utf-8")
        # Preview deployments should not appear in search results. The preview
        # hostname is separate from the canonical production domain.
        (staged / "_headers").write_text(
            "https://:worker.justin-smethers.workers.dev/*\n"
            "  X-Robots-Tag: noindex\n"
            "/*\n"
            "  X-Content-Type-Options: nosniff\n",
            encoding="utf-8",
        )
        # Keep the database, credentials and Markdown sources out of the export.
        if output.exists():
            shutil.rmtree(output)
        shutil.copytree(staged, output)

    print(f"Built {len(posts)} posts and the blog index in {output}")


if __name__ == "__main__":
    main()
