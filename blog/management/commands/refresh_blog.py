from django.core.management.base import BaseCommand
from blog.models import BlogPost
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Refreshes all blog entries.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting the blog refresh process...'))

        # Step A: Delete current entries
        BlogPost.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all current blog entries.'))

        # Step B: Fetch and populate new entries
        call_command('fetch_github_md')
        self.stdout.write(self.style.SUCCESS('Blog entries have been updated with latest content.'))
