# 初次配置

询问用户 `agent-kit` 的期望本地路径、仓库 URL 和分支，将这些信息保存到 `~/.agent-kit`，然后拉取仓库并切换到指定分支。文件格式与 `scripts/sync.py` 一致：

```json
{"path":"/path/to/agent-kit","url":"仓库 URL","branch":"main"}
```
