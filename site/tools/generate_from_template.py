import sys
import os

if len(sys.argv) != 2:
    raise ValueError("CLI usage: python generate_from_template.py <project_name>")

project = sys.argv[1]

os.makedirs("_generated", exist_ok=True)

with open("analysis_template.md", "r") as fh:
    template = fh.read()
with open(f"_generated/{project}.md", "w") as fh:
    fh.write(template.replace("{{ project }}", project))
