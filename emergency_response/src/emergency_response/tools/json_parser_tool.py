import json
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Type

from crewai_tools import BaseTool
from pydantic import BaseModel

from emergency_response.src.emergency_response.tools.schemas.json_parser_schema import JSONParserSchema


class JSONParserTool(BaseTool):
    """
    A tool that reads a JSON file with fire truck or hospital units.
    """
    name: str = "JSONReaderTool"
    description: str = "A tool that reads a JSON file with fire truck or hospital units."
    args_schema: Type[BaseModel] = JSONParserSchema
    json_file_path: Optional[str] = None
    json_file_type: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(
            self,
            json_file_type: Literal["fire_trucks", "hospitals"] = "fire_trucks",
            **kwargs: Any,
    ):
        super().__init__(**kwargs)

        # Base directory for the project
        base_dir = Path(__file__).resolve().parents[3] / "data"

        # Determine the file path based on the file type
        if json_file_type == "hospitals":
            self.json_file_path = base_dir / "hospitals.json"
        elif json_file_type == "fire_trucks":
            self.json_file_path = base_dir / "firetrucks.json"
        else:
            raise ValueError(
                "Invalid json_file_type: should be one of 'fire_trucks' or 'hospitals'."
            )

        self.json_file_type = json_file_type

    def _read_json(self) -> List[Dict[str, Any]]:
        """
        Reads the JSON file and returns the content.
        """
        try:
            with open(self.json_file_path, "r") as file:
                data = json.load(file)

            # Ensure the structure is a list
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and self.json_file_type in data:
                return data[self.json_file_type]  # Handle nested JSON
            else:
                raise ValueError(f"Unexpected JSON structure: {data}")

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.json_file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON file: {e}")

    def _run(self, *args: Any, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        Runs the JSON parsing logic and returns the parsed content.
        """
        return self._read_json()
