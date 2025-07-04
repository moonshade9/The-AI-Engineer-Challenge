from aimakerspace.text_utils import MarkdownLoader
import os

# Create a sample markdown file for testing
sample_md_path = "tests/sample_test.md"
sample_content = """\
# Test Markdown

This is a test file.

- Item 1
- Item 2
"""

# Write the sample markdown file if it doesn't exist
if not os.path.exists(sample_md_path):
    with open(sample_md_path, "w", encoding="utf-8") as f:
        f.write(sample_content)

# Test the MarkdownLoader
loader = MarkdownLoader(sample_md_path)
loader.load()
docs = loader.documents

print("Loaded documents:")
for doc in docs:
    print(doc) 