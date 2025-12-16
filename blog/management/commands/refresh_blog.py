import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from blog.models import BlogPost

class Command(BaseCommand):
    help = 'Refreshes all blog entries.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting the blog refresh process...'))

        # Step A: Delete current entries
        BlogPost.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all current blog entries.'))

        use_local = os.environ.get("USE_LOCAL_BLOG_POSTS") == "1"
        github_vars = ("GITHUB_USERNAME", "GITHUB_REPO", "GITHUB_BRANCH", "GITHUB_BLOG_POSTS_FILEPATH")
        missing_github = [var for var in github_vars if not os.environ.get(var)]

        if use_local or missing_github:
            if missing_github and not use_local:
                self.stdout.write(self.style.WARNING(
                    f"Missing GitHub env vars {missing_github}; loading posts from local 'blog_posts/'."
                ))
            call_command('load_local_posts')
        else:
            # Step B: Fetch and populate new entries from GitHub
            call_command('fetch_github_md')

        self.stdout.write(self.style.SUCCESS('Blog entries have been updated with latest content.'))
