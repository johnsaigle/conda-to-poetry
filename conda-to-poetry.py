import argparse
import toml
from typing import Dict, Any
import re

def conda_to_poetry(conda_pyproject: str) -> str:
    """
    Convert a conda-style pyproject.toml to Poetry format.
    
    Args:
        conda_pyproject: Content of the conda pyproject.toml file
    
    Returns:
        Poetry-formatted pyproject.toml content
    """
    # Parse the input TOML
    config = toml.loads(conda_pyproject)
    
    # Initialize Poetry structure
    poetry_config = {
        "tool": {
            "poetry": {
                "name": "",
                "version": "",
                "description": "",
                "authors": [],
                "dependencies": {},
                "dev-dependencies": {}
            }
        },
        "build-system": {
            "requires": ["poetry-core>=1.0.0"],
            "build-backend": "poetry.core.masonry.api"
        }
    }
    
    # Map project metadata
    if "project" in config:
        project = config["project"]
        poetry_config["tool"]["poetry"].update({
            "name": project.get("name", ""),
            "version": project.get("version", "0.1.0"),
            "description": project.get("description", ""),
            "authors": project.get("authors", []),
        })
        
        # Convert dependencies
        if "dependencies" in project:
            for dep in project["dependencies"]:
                if isinstance(dep, str):
                    # Handle simple dependencies
                    name = re.split('[><=~!]', dep)[0].strip()
                    poetry_config["tool"]["poetry"]["dependencies"][name] = _convert_version_spec(dep)
                elif isinstance(dep, dict):
                    # Handle complex dependencies
                    for name, spec in dep.items():
                        poetry_config["tool"]["poetry"]["dependencies"][name] = _convert_complex_spec(spec)
        
        # Convert optional-dependencies to extras
        if "optional-dependencies" in project:
            poetry_config["tool"]["poetry"]["extras"] = {}
            for group, deps in project["optional-dependencies"].items():
                converted_deps = {}
                for dep in deps:
                    name = re.split('[><=~!]', dep)[0].strip()
                    converted_deps[name] = _convert_version_spec(dep)
                poetry_config["tool"]["poetry"]["extras"][group] = converted_deps

    return toml.dumps(poetry_config)

def _convert_version_spec(spec: str) -> str:
    """Convert conda version specification to Poetry format."""
    if not any(op in spec for op in ['>', '<', '=', '~', '!']):
        return "*"
    
    # Replace common conda version patterns with Poetry equivalents
    spec = re.sub(r'>=(\d+\.\d+\.\d+),<(\d+\.\d+\.\d+)', r'>=$1,<$2', spec)
    spec = spec.replace('~=', '^')
    return spec

def _convert_complex_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Convert complex dependency specifications."""
    poetry_spec = {}
    
    if "version" in spec:
        poetry_spec["version"] = _convert_version_spec(spec["version"])
    
    if "python" in spec:
        poetry_spec["python"] = _convert_version_spec(spec["python"])
    
    if "extras" in spec:
        poetry_spec["extras"] = spec["extras"]
    
    if "source" in spec:
        if spec["source"] == "git":
            poetry_spec["git"] = spec.get("url", "")
            if "rev" in spec:
                poetry_spec["rev"] = spec["rev"]
        elif spec["source"] == "url":
            poetry_spec["url"] = spec.get("url", "")
    
    return poetry_spec

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--file", type=argparse.FileType('r'), help="conda file")

    args = parser.parse_args()

    print(conda_to_poetry(''.join(args.file.readlines())))


if __name__ == "__main__":
    main()
