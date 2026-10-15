# 组织约定

## 目录

每个 skill 固定两层：`skills/<分类>/<skill>/`。

- `global`：保留分类，存放常驻全局链接的 skill（如 agent-kit-manager 自身）。
- 其他分类：按主题生长，名称与数量由用户与 agent 决定，不预设、不固定。
- 新增 skill 时先列出现有分类，能归入就归入；没有合适的才新建分类，并与用户确认分类名。
- 需要常驻全局时把 skill 移入 `global`；不再常驻的移回主题分类。

## 存储形态

- 自用沉淀：直接放 kit 目录。
- 独立仓库（自己的或第三方的）：git submodule。
- 其他来源：下载后放入，并在 `<skill>/source.md` 记录来源 URL。

## 链接

- 全局：`<agent 全局 skill 目录>/<skill>` → `<kit>/skills/global/<skill>`。
- 项目：`<工程>/.agents/skills/<skill>` → `<kit>/skills/<分类>/<skill>`；默认放仓库根，模块级需求可放子目录。Codex 从当前目录向上扫描到仓库根，并跟随软链接。
- 链接默认只留在本机，不提交到工程仓库。
- 分类或路径调整后，修复所有受影响的链接。

## 检索

运行 `scripts/list.py` 输出 kit 的 JSON 目录（name、分类、描述、路径、存储形态），用于检索与引入。
