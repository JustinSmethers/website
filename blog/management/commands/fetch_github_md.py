from django.core.management.base import BaseCommand
from github import Github
from blog.models import BlogPost
import markdown2
import yaml
import re
import os

class Command(BaseCommand):
    help = 'Fetches markdown files from a GitHub repository'
    
    def handle(self, *args, **kwargs):
        g = Github(os.environ.get('GITHUB_TOKEN'))
        repo = g.get_repo(f"{os.environ.get('GITHUB_USERNAME')}/{os.environ.get('GITHUB_REPO')}")
        branch_ref = repo.get_branch(os.environ.get('GITHUB_BRANCH'))

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
        thumbnail_url = self.get_file_url(dir_path, metadata.get('thumbnail', ''), repo, branch_ref)

        # Replace local image paths with absolute URLs
        content = self.replace_image_paths(content, dir_path, repo, branch_ref)

        BlogPost.objects.update_or_create(
            title=metadata['title'],
            defaults={
                'description': metadata.get('description', ''),
                'content': markdown2.markdown(content),
                'thumbnail': thumbnail_url,
            }
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
            img_url = self.get_file_url(dir_path, img_path, repo, branch_ref)
            return f"![{alt_text}]({img_url})"

        return re.sub(pattern, replace, content)

    def get_file_url(self, dir_path, filename, repo, branch_ref):
        if filename:
            try:
                file = repo.get_contents(f"{dir_path}/{filename}", ref=branch_ref.commit.sha)
                return file.download_url
            except:
                return None
        return ''
