# 初次配置

询问用户是否已有自己的 `agent-kit` 仓库；若已有，获取仓库 URL，若没有，先按用户选择的托管位置创建。再询问期望的本地路径和分支，将路径、仓库 URL、分支保存到 `~/.agent-kit`，然后拉取仓库并切换到指定分支。文件格式与 `scripts/sync.py` 一致：

```json
{"path":"/path/to/agent-kit","url":"仓库 URL","branch":"main"}
```
