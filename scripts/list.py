#!/usr/bin/env python3
"""Scan the whole kit for skills and print the catalog as JSON for the calling agent."""

import json
import re
import subprocess
from pathlib import Path

FRONTMATTER_PATTERN = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*\n", re.DOTALL)
FIELD_PATTERN = re.compile(r"^([A-Za-z0-9_-]+):[ \t]*(.*)$")
BLOCK_PATTERN = re.compile(r"^([A-Za-z0-9_-]+):[ \t]*([|>][-+0-9]*)[ \t]*$")


def emit(payload):
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def parse_frontmatter(text):
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return {}
    lines = match.group(1).splitlines()
    fields = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        block = BLOCK_PATTERN.match(line)
        if block:
            key, style = block.group(1), block.group(2)
            parts = []
            index += 1
            while index < len(lines) and (not lines[index].strip() or lines[index][:1] in (" ", "\t")):
                parts.append(lines[index].strip())
                index += 1
            joiner = "\n" if style.startswith("|") else " "
            fields[key] = joiner.join(part for part in parts if part)
            continue
        field = FIELD_PATTERN.match(line)
        if field:
            value = field.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            fields[field.group(1)] = value
        index += 1
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

    if not path.is_dir():
        emit({"message": f"未找到 kit 目录 {path}；请检查 ~/.agent-kit 配置。"})
        return

    skills_root = path / "skills"
    submodules = submodule_paths(path)
    skills = []
    for skill_md in sorted(path.rglob("SKILL.md")):
        if ".git" in skill_md.relative_to(path).parts:
            continue
        skill_dir = skill_md.parent
        relative = skill_dir.relative_to(path).as_posix()
        parent = skill_dir.parent
        try:
            category = parent.relative_to(skills_root).as_posix()
        except ValueError:
            category = parent.relative_to(path).as_posix()
        if category == ".":
            category = ""
        fields = parse_frontmatter(skill_md.read_text(encoding="utf-8", errors="replace"))
        source_file = skill_dir / ".source.json"
        if relative in submodules:
            form = "submodule"
        elif source_file.is_file():
            form = "download"
        else:
            form = "dir"
        entry = {
            "name": fields.get("name", skill_dir.name),
            "category": category,
            "path": relative,
            "description": fields.get("description", ""),
            "form": form,
        }
        if source_file.is_file():
            try:
                source = json.loads(source_file.read_text(encoding="utf-8")).get("source")
                if isinstance(source, str) and source:
                    entry["source"] = source
            except (OSError, ValueError, TypeError):
                pass
        skills.append(entry)

    emit({"kit": str(path), "skills": skills})


if __name__ == "__main__":
    main()
