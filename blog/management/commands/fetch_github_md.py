import os
import sys
import django
from datetime import date, datetime
from django.utils import timezone
from django.utils.safestring import mark_safe


# Adjust these paths and names to fit your project structure and settings
project_path = '/home/justin/website'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'buzzz.settings')

# Include the project path in the Python path
sys.path.append(project_path)

# Initialize Django
django.setup()


from django.core.management.base import BaseCommand
from github import Github
from blog.models import BlogPost
from blog.tagging import ALLOWED_TAGS, normalize_and_validate_tags
import markdown
import yaml
import re

class Command(BaseCommand):
    help = 'Fetches markdown files from a GitHub repository'
    
    def handle(self, *args, **kwargs):
        g = Github(os.environ.get('GITHUB_TOKEN'))
        repo = g.get_repo(f"{os.environ.get('GITHUB_USERNAME')}/{os.environ.get('GITHUB_REPO')}")
        branch_ref = repo.get_branch(os.environ.get('GITHUB_BRANCH'))
        self.base_url = f"https://{os.environ.get('GITHUB_USERNAME')}.github.io/{os.environ.get('GITHUB_REPO')}"

        directories = repo.get_contents(path=os.environ.get('GITHUB_BLOG_POSTS_FILEPATH'), ref=branch_ref.commit.sha)
        for directory in directories:
            print('DIRECTORY', directory)
            print(f'Found directory: {directory.path}')
            if directory.type == 'dir':
                files = repo.get_contents(path=directory.path, ref=branch_ref.commit.sha)
                md_file = next((file for file in files if file.name.endswith('.md')), None)
                if md_file:
                    self.process_markdown_file(md_file, directory.path, repo, branch_ref)

    def process_markdown_file(self, md_file, dir_path, repo, branch_ref):
        content = md_file.decoded_content.decode()
        metadata, content = self.parse_markdown(content)
        thumbnail_url = self.get_file_url(dir_path, metadata.get('thumbnail', ''))

        # Replace local image paths with absolute URLs
        content = self.replace_image_paths(content, dir_path, repo, branch_ref)

        md_file_name = md_file.name.strip(".md")
        
        # Specify the Markdown extensions to use
        extensions = [
            "markdown.extensions.fenced_code",      # Allows code blocks to be fenced by ``` or ~~~
            "markdown.extensions.tables",           # Allows tables to be created using | and -
            "markdown.extensions.toc",              # Allows a table of contents to be generated
            "markdown.extensions.codehilite",       # Allows syntax highlighting
            "markdown.extensions.sane_lists",       # Allows lists to be created without preceding blank lines
            "markdown.extensions.extra"             # Adds several miscellaneous extensions
        ]

        # Specify the configuration for each extension
        extension_configs = {
            # "codehilite": {
            #     'use_pygments': True,
            #     'css_class': 'language-python'
            #     # 'css_class': 'codehilite',
            #     # 'pygments_style': 'github-dark',
            #     # 'noclasses': True
            # },
        }

        # Create a Markdown instance
        md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)

        # Convert the Markdown content to HTML
        content = mark_safe(md.convert(content))

        normalised_tags, invalid_tags = normalize_and_validate_tags(metadata.get('tags'))
        if invalid_tags:
            source = getattr(md_file, "path", md_file.name)
            self.stdout.write(
                self.style.WARNING(
                    f"Ignoring disallowed tag(s) {invalid_tags} in '{source}'. "
                    f"Allowed tags: {', '.join(ALLOWED_TAGS)}"
                )
            )

        defaults = {
            'description': metadata.get('description', ''),
            'content': content,
            'thumbnail': thumbnail_url,
            'post_name': md_file_name,
            'tags': normalised_tags,
        }

        post_date = self.parse_post_date(metadata.get('date'))
        if post_date:
            defaults['date_posted'] = post_date

        BlogPost.objects.update_or_create(
            title=metadata['title'],
            defaults=defaults
        )

    def parse_markdown(self, content):
        # Split YAML front matter and Markdown content
        if content.startswith("---"):
            parts = content.split('---', 2)
            metadata = yaml.safe_load(parts[1])
            content = parts[2]
        else:
            metadata = {}
        return metadata, content    

    def replace_image_paths(self, content, dir_path, repo, branch_ref):
        # Regular expression to find Markdown image syntax
        pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
        
        # Replace the relative paths
        def replace(match):
            alt_text, img_path = match.groups()
            # Use get_file_url to get the absolute URL
            img_url = self.get_file_url(dir_path, img_path)
            print('IMAGE URL', img_url)
            return f"![{alt_text}]({img_url})"

        return re.sub(pattern, replace, content)

    def get_file_url(self, dir_path, filename):
        if filename:
            return f'{self.base_url}/{dir_path}/{filename}'
        return ''

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
