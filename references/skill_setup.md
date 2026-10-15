# 引入与创建 Skill

先判断归属：只适用于当前工程的 skill 直接在工程中处理；可跨工程复用的默认进入 kit，除非用户明确要求只放本地。

目录、分类与链接规则见 [organization.md](organization.md)。

## 从 kit 引入

适用于新建工程或工程需要能力补充时。

1. 运行 `scripts/list.py`，读取 kit 全部 skill 的 JSON 目录。
2. 结合当前工程特征（语言、框架、目录结构、依赖、AGENTS.md 等）挑选候选，向用户给出建议与理由。
3. 用户确认后建立链接：常驻全局的用 `global` 分类，项目使用的链接到 `<工程>/.agents/skills/<skill>`。

## 创建并入库

1. 起草 skill（环境中有 skill-creator 时使用它），确定名称与描述。
2. 按 [organization.md](organization.md) 确定存储形态与分类：独立 git 仓库用 submodule；其他来源下载放入，并在 `<skill>/source.md` 记录来源 URL。
3. 放入 `skills/<分类>/<skill>/`，需要时链接到目标作用域。
4. 提交并推送 kit 仓库变更。
