from pathlib import Path
from crewai_tools import BaseTool
from emergency_response.src.emergency_response.tools.schemas.mdx_parser_schema import FireEventSchema
from typing import Optional, Type

class MDXParserTool(BaseTool):
    """
    A CrewAI tool for parsing MDX files to extract fire event details.
    """

    name: str = "MDXParser"
    description: str = (
        "A tool for parsing MDX files to extract fire event details such as fire type, "
        "coordinates, severity, and the number of injured people."
    )
    args_schema: Type[FireEventSchema] = FireEventSchema  # Use the input schema
    default_path: Path = None  # Define default_path as a field

    def __init__(self, **kwargs):
        """
        Initializes the MDXParser and sets the default file path.
        """
        super().__init__(**kwargs)
        base_dir = Path(__file__).resolve().parents[3]  # Adjust based on project structure
        object.__setattr__(self, "default_path", base_dir / "data" / "emergency_01.mdx")  # Assign directly to avoid validation issues

    def _run(self, file_path: Optional[str] = None) -> dict:
        """
        Parses the MDX file to extract fire event details.

        Args:
            file_path (str): Optional path to the MDX file (overrides default_path).

        Returns:
            dict: Parsed fire event details.
        """
        file_path = Path(file_path) if file_path else self.default_path

        try:
            # Read the file content
            with open(file_path, "r") as file:
                file_content = file.read()

            # Parse the content
            fire_details = {}
            lines = file_content.splitlines()
            for line in lines:
                line = line.strip()
                if "Fire Type:" in line:
                    # Remove unwanted characters like '*'
                    fire_details["fire_type"] = line.split(":")[1].strip().lstrip("*").strip()
                elif "X, Y Coordinates" in line:
                    coords = line.split("(")[0].strip()
                    fire_details["x_location"], fire_details["y_location"] = map(float, coords.split(","))
                elif "Number of Injured People:" in line:
                    injured = line.split(":")[1].strip()
                    fire_details["injured_people"] = int("".join(filter(str.isdigit, injured)))
                elif "Fire Severity:" in line:
                    # Remove unwanted characters like '*'
                    fire_details["severity"] = line.split(":")[1].strip().lstrip("*").strip()

            # Validate and return details using the FireEventDetails schema
            return FireEventSchema(**fire_details).dict()

        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File not found at {file_path}")
        except Exception as e:
            raise RuntimeError(f"Error parsing MDX file: {e}")



