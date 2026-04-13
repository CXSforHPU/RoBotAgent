from env import (
    SKILLS_PATH
)
import re
import json
from typing import (
    Dict
)


class Skills:
    def __init__(self):
        self.__skills_path = SKILLS_PATH

    def __len__(self):
        return len(self.list())

    def list(self):
        skills = []

        if not self.__skills_path.exists():
            return skills

        for skill in self.__skills_path.iterdir():
            if not skill.is_dir():
                continue

            skill_file = skill / "SKILL.md"
            if not skill_file.exists():
                continue

            skills.append({
                "name": skill.name,
                "path": str(skill_file),
            })

        return skills

    def load_skills(self, name: str) -> str | None:
        skill_file = self.__skills_path / name / "SKILL.md"
        if not skill_file.exists():
            return None

        return skill_file.read_text(encoding="utf-8")

    def get_skill_metadata(self, name: str) -> Dict | None:
        content = self.load_skills(name)
        if content is None:
            return None

        if not content.startswith("---"):
            return None

        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if match is None:
            return None

        metadata = {}
        for line in match.group(1).split("\n"):
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"\"')

        if "metadata" in metadata:
            try:
                metadata["metadata"] = json.loads(metadata["metadata"])
            except json.decoder.JSONDecodeError:
                metadata["metadata"] = {}
        return metadata

    def get_skill_description(self, name: str) -> str:
        metadata = self.get_skill_metadata(name)
        if metadata and metadata.get("description"):
            return metadata["description"]
        return name

    def summary(self) -> str:
        skills = self.list()
        if not skills:
            return ""

        lines = ["<skills>"]
        for skill in skills:
            name = self.escape_xml(skill["name"])
            path = skill["path"]
            description = self.escape_xml(self.get_skill_description(skill["name"]))
            available = True

            lines.append(" " * 2 + f"<skill available=\"{str(available).lower()}\">")
            lines.append(" " * 4 + f"<name>{name}</name>")
            lines.append(" " * 4 + f"<description>{description}</description>")
            lines.append(" " * 4 + f"<location>{path}</location>")
            lines.append(" " * 2 + f"</skill>")
        lines.append("</skills>")
        return "\n".join(lines)

    @staticmethod
    def escape_xml(text: str) -> str:
        return text.replace(
            "&", "&amp;"
        ).replace(
            "<", "&lt;"
        ).replace(
            ">", "&gt;"
        )