#!/usr/bin/env python3
"""Read the local agent-kit location and sync its configured branch."""

import json
import subprocess
from pathlib import Path


def report(message, config=None):
    result = {"message": message}
    if config is not None:
        result["agent_kit"] = config
    print(json.dumps(result, ensure_ascii=False))


def git(path, *args):
    result = subprocess.run(
        ["git", "-C", str(path), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Git 执行失败")
    return result.stdout.strip()


def main():
    config_path = Path.home() / ".agent-kit"
    if not config_path.is_file():
        report("未找到 ~/.agent-kit；请执行 setup.md。")
        return

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        path = Path(config["path"]).expanduser()
        branch = config["branch"]
        url = config["url"]
        if not all(isinstance(item, str) and item for item in (config["path"], branch, url)):
            raise ValueError("path、url 和 branch 必须是非空字符串")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report(f"无法读取 ~/.agent-kit：{exc}；请执行 setup.md。")
        return

    if not (path / ".git").exists():
        report("仓库路径尚未拉取；请执行 setup.md。", config)
        return

    try:
        remote = git(path, "remote", "get-url", "origin")
        if remote != url:
            raise RuntimeError(f"origin 为 {remote}，与 ~/.agent-kit 中的 URL 不同")
        current = git(path, "branch", "--show-current")
        if current != branch:
            raise RuntimeError(f"当前分支是 {current or '游离 HEAD'}，预期为 {branch}")
        git(path, "pull", "--ff-only", "origin", branch)
    except (OSError, RuntimeError) as exc:
        report(f"同步未完成：{exc}。请检查并处理后重新运行 sync.py。", config)
        return

    report("同步成功。", config)


if __name__ == "__main__":
    main()
