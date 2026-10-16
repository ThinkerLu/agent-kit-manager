# 组织约定

## 目录

不限制 skill 的位置与层级：`scripts/list.py` 会递归扫描整个 kit 的 `SKILL.md`，放在任何位置都能被检索到。

- 尽量模仿现有结构、就近归类（如 `skills/global/`、`skills/kb/`、`skills/cloudmusic/<子类>/`）。
- `global`：初始约定分类，存放常驻全局链接的 skill（如 agent-kit-manager 自身）；需要常驻全局时移入 `global`，不再常驻的移回主题分类。
- 其他分类：按主题生长，名称与数量由用户与 agent 决定，不预设、不固定。
- 新增 skill 时先列出现有结构，能归入就归入；没有合适的再新建，并与用户确认名字。

## 存储形态

- 自用沉淀：直接放 kit 目录。
- 独立仓库（自己的或第三方的）：git submodule；在其内部修改前先 `git switch main`（submodule 默认停在 detached HEAD），推送后在 kit 内提交新的指针。
- 其他来源：下载后放入，并在 `<skill>/source.md` 记录来源 URL。

## 链接

- 全局：`<agent 全局 skill 目录>/<skill>` → `<kit>/skills/global/<skill>`。
- 项目：`<工程>/.agents/skills/<skill>` → kit 内该 skill 的实际位置；默认放仓库根，模块级需求可放子目录。Codex 从当前目录向上扫描到仓库根，并跟随软链接。
- 链接默认只留在本机，不提交到工程仓库。
- skill 的位置调整后，修复所有受影响的链接。

## 检索

运行 `scripts/list.py`：递归扫描整个 kit，输出 JSON 目录（name、分类、描述、路径、存储形态），用于检索与引入。
