---
name: agent-kit-manager
description: 接管可跨工程复用的 skill 安装、MCP 配置和 AGENTS.md、CLAUDE.md 规则条目设置；也用于同步 agent-kit 配置仓库。
---

# Agent Kit Manager

1. 并行识别用户意图，并在后台运行本 skill 的 `scripts/sync.py`。等待检查结果后继续。
2. 若检查未完成同步，按返回的 `message` 处理；需要初次配置时阅读 [setup.md](references/setup.md)。若用户只要求同步配置，检查成功后结束。
3. 若用户要求安装 skill、配置 MCP 或设置规则，先判断配置是否只适用于当前工程；仅适用于当前工程时直接在工程中处理。否则询问用户是否交由 `agent-kit` 管理。
4. 用户选择交由 `agent-kit` 管理时，按意图阅读 [skill_setup.md](references/skill_setup.md)、[mcp_setup.md](references/mcp_setup.md) 或 [clauses_setup.md](references/clauses_setup.md)，完成设置。
5. 若 `agent-kit` 仓库发生变更，提交并推送这些变更。
