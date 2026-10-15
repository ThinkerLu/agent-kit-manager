#!/usr/bin/env python3
"""Print the agent-kit skill catalog as JSON for the calling agent."""

import json
import re
import subprocess
from pathlib import Path

FRONTMATTER_PATTERN = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*\n", re.DOTALL)
FIELD_PATTERN = re.compile(r"^([A-Za-z0-9_-]+):[ \t]*(.*)$")


def emit(payload):
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def parse_frontmatter(text):
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        field = FIELD_PATTERN.match(line)
        if field:
            value = field.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            fields[field.group(1)] = value
    return fields


def submodule_paths(kit):
    result = subprocess.run(
        ["git", "-C", str(kit), "config", "-f", ".gitmodules", "--get-regexp", "path$"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        return set()
    paths = set()
    for line in result.stdout.splitlines():
        _, _, value = line.partition(" ")
        paths.add(value.strip())
    return paths


def main():
    config_path = Path.home() / ".agent-kit"
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(config.get("path"), str) or not config["path"]:
            raise ValueError("path 必须是非空字符串")
        path = Path(config["path"]).expanduser()
    except (OSError, ValueError, TypeError) as exc:
        emit({"message": f"无法读取 ~/.agent-kit：{exc}；请执行 setup.md。"})
        return

    skills_root = path / "skills"
    if not skills_root.is_dir():
        emit({"message": f"未找到 {skills_root}；请检查 kit 目录结构。"})
        return

    submodules = submodule_paths(path)
    skills = []
    for skill_md in sorted(skills_root.glob("*/*/SKILL.md")):
        skill_dir = skill_md.parent
        relative = skill_dir.relative_to(path).as_posix()
        fields = parse_frontmatter(skill_md.read_text(encoding="utf-8", errors="replace"))
        if relative in submodules:
            form = "submodule"
        elif (skill_dir / "source.md").is_file():
            form = "download"
        else:
            form = "dir"
        skills.append(
            {
                "name": fields.get("name", skill_dir.name),
                "category": skill_dir.parent.name,
                "path": relative,
                "description": fields.get("description", ""),
                "form": form,
            }
        )

    emit({"kit": str(path), "skills": skills})


if __name__ == "__main__":
    main()
