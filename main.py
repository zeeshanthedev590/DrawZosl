import re
from jinja2 import Environment, FileSystemLoader

def remove_comments(input_content):
    # Remove single-line comments starting with "//"
    return re.sub(r"\/\/.*$", "", input_content, flags=re.MULTILINE)

def tokenize(input_content):
    lines = input_content.splitlines()
    tokens = []
    groups = {}
    relationships = []
    token_regex = r"(@[\w-]+(?:\([^)]*\))?| *\[[^\]]*\]| *-> *)"

    current_group = None
    for line in lines:
        trimmed_line = line.strip()
        if not trimmed_line:
            continue  # Skip empty lines

        if trimmed_line.startswith("@"):
            # If it's a group or relationship, set it as the current group or add it to relationships
            if "->" in trimmed_line:
                relationships.append(trimmed_line)
            else:
                current_group = re.sub(r"\(.*\)", "", trimmed_line).strip("@")
                groups[current_group] = {"fields": []}
        elif trimmed_line == "$end" + current_group:
            # If it's the end of a group, clear the currentGroup
            current_group = None
        elif trimmed_line.startswith("["):
            # If it's a field, add it to the current group's fields
            field_content = trimmed_line[1:-1].strip()
            # Skip adding commented fields to the group's fields
            if not field_content.startswith("//"):
                groups[current_group]["fields"].append(field_content)

        tokens.append(trimmed_line)

    return {"tokens": tokens, "groups": groups, "relationships": relationships}

def generate_html(groups, relationships):
    # Load Jinja templates from a "templates" folder
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("defualt.html")

    # Render the template with the provided data
    html_content = template.render(groups=groups, relationships=relationships)

    return html_content

def read_input_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def main():
    # Replace "example.zosl" with the path to your local ZOSL file
    input_file = "example.zosl"

    input_content = read_input_file(input_file)
    parsed_data = tokenize(remove_comments(input_content))
    html_content = generate_html(parsed_data["groups"], parsed_data["relationships"])

    # Write the HTML content to a local file
    output_file = "output.html"
    with open(output_file, "w") as file:
        file.write(html_content)

    print(f"HTML file generated: {output_file}")

if __name__ == "__main__":
    main()
