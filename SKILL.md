---
name: agent-kit-manager
description: 管理 agent-kit 配置仓库与跨工程复用资产：从 kit 检索并引入合适的 skill 到工程、把可复用 skill 创建入库、整理 kit 分类，以及配置 MCP、AGENTS.md、CLAUDE.md 规则条目；也用于同步 agent-kit 仓库。
---

# Agent Kit Manager

`agent-kit`（`~/.agent-kit` 指向的仓库）是跨工程复用资产的唯一存放处；本机各 agent 的 skill 目录只放链接。

1. 识别用户意图，并在后台运行本 skill 的 `scripts/sync.py`。等待结果后继续。
2. 若同步未完成，按返回的 `message` 处理；需要初次配置时阅读 [setup.md](references/setup.md)。若用户只要求同步，成功后结束。
3. 按意图进入对应流程；skill 的目录、分类与链接规则以 [organization.md](references/organization.md) 为准：
   - 检索并引入（新建工程或工程需要能力补充时）：运行 `scripts/list.py` 读取 kit 的 JSON 目录，结合当前工程特征给出候选与理由，用户确认后建立链接。
   - 创建并入库：可复用的默认存入 kit。
   - 整理分类：调整 kit 内 skill 的分类与路径，并同步修复相关链接。
   - 配置 MCP：阅读 [mcp_setup.md](references/mcp_setup.md)；设置规则条目：阅读 [clauses_setup.md](references/clauses_setup.md)。
4. 引入与创建的具体步骤阅读 [skill_setup.md](references/skill_setup.md)；只适用于当前工程的内容直接在工程中处理，不进入 kit。
5. 若 `agent-kit` 仓库发生变更，提交并推送这些变更。
