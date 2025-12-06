import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Template

class StringManager:
  def __init__(self, prompts_dir: str = "resources/texts"):
    base_dir = Path(__file__).parent.parent.parent
    prompts_path = Path(prompts_dir)
    if not prompts_path.is_absolute():
      prompts_path = base_dir / prompts_path
    self.text_dir = prompts_path.resolve()
    self.string_resource_map: Dict[str, Dict[str, Any]] = {}
    self._load_all_text_resources()

  def _load_all_text_resources(self):
    yaml_files = list(self.text_dir.rglob("*.yml"))
    for file_path in yaml_files:
      with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        string_resource_name = data.get("name")
        if not string_resource_name:
          continue
        versions = data.get("versions", [])
        if not versions:
          continue
        self.string_resource_map[string_resource_name] = {
          "versions": versions,
          "default_version": data.get("default_version", versions[-1]["version"])
        }

  def get(self, item, **kwargs):
    return Template(self.get_text_resource(item)).render(**kwargs)

  def get_text_resource(
      self,
      string_name: str,
      version: Optional[int] = None,
      alias: Optional[str] = None,
  ) -> str:
    string_entry = self.string_resource_map.get(string_name)
    if not string_entry:
      raise ValueError(f"Prompt '{string_name}' not found")

    versions = string_entry["versions"]

    string_resource = None
    if alias:
      string_resource = next((v for v in versions if v.get("alias") == alias), None)
    if not string_resource and version is not None:
      string_resource = next((v for v in versions if v.get("version") == version), None)
    if not string_resource:
      default_version = string_entry.get("default_version", versions[-1]["version"])
      string_resource = next((v for v in versions if v.get("version") == default_version), versions[-1])

    template_text = string_resource["template"]

    return template_text

string_manager = StringManager()
