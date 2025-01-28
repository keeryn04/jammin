import os

file_path = input("Enter the component path: ")
if file_path == "":
    file_path = "frontend/src/components"


def generate_component(component_name):
    component_name = component_name.capitalize()
    component_path = f"{file_path}/{component_name}"
    # Create the component folder
    if not os.path.exists(component_path):
        os.makedirs(component_path)
    else:
        print("Component already exists")
        return

    # Create the index.js file
    index_file = open(f"{component_path}/index.js", "w")
    # Make the index.js file export the component
    index_file.write(f"import {component_name} from './{component_name}';\n\nexport default {component_name};")
    index_file.close()


    # Create the SCSS file
    scss_file = open(f"{component_path}/{component_name}.scss", "w")
    # Make the SCSS file import the app.scss file
    scss_file.write(f"@import \"./../../app.scss\";\n\n.{component_name} {{\n  \n}}")

    scss_file.close()

    # Create the JSX file
    jsx_file = open(f"{component_path}/{component_name}.jsx", "w")
    jsx_file.write(f"import React from 'react';\n\nfunction {component_name}() {{\n  return (\n    <div>\n      <h1>{component_name}</h1>\n    </div>\n  );\n}}\n\nexport default {component_name};")
    jsx_file.close()

if __name__ == "__main__":
    component_name = input("Enter the name of the component: ")
    generate_component(component_name)
