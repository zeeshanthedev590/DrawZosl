import random

# Function to generate a random group name
def generate_group_name():
    return f"@Group{random.randint(1, 1000)}"

# Function to generate a random field name
def generate_field_name():
    return f"[field{random.randint(1, 1000)}]"

# Function to generate a random ZOSL group with 5 fields
def generate_group():
    group_name = generate_group_name()
    fields = [generate_field_name() for _ in range(5)]
    group_content = f"{group_name}\n"
    group_content += "\n".join(fields) + "\n"
    group_content += f"$end{group_name}\n\n"
    return group_content

# Generate 10 ZOSL groups
zosl_content = ""
for _ in range(10):
    zosl_content += generate_group()

# Save the content to a file
with open("sample.zosl", "w") as file:
    file.write(zosl_content)

print("Sample ZOSL file 'sample.zosl' generated with 10 groups.")

