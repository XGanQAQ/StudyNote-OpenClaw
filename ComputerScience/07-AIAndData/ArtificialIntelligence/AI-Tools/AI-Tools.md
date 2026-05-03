# AI 辅助编程工具

## 工具对比

| 工具 | 类型 | 特点 |
|------|------|------|
| Cursor | AI IDE | VS Code 分支、内嵌 AI 对话、代码补全 |
| Windsurf | AI IDE | 类似 Cursor，Cascade 模式 |
| Claude Code | CLI Agent | Anthropic 出，终端里自主编程 |
| GitHub Copilot Codex | CLI/API | OpenAI 出，Agent 模式 |
| Aider | CLI | 开源，支持多种 LLM |

## AI IDE vs AI Tool 区别

| 维度 | AI IDE (Cursor/Windsurf) | AI Tool (Claude Code/Codex) |
|------|------------------------|----------------------------|
| 使用方式 | 图形界面 | 命令行终端 |
| 上手 | 低（习惯 IDE 即可） | 需习惯 CLI 操作 |
| 深入修改 | 拖拽/点击可见代码 | 需指令指定范围 |
| 适合场景 | 日常开发、探索 | 大规模重构、自动化 |

## 文档设计先行的工作流
> 先写文档/设计 → 再交给 AI 生成代码

优势：
1. 明确需求边界
2. 提供上下文给 AI
3. 文档即 test case
4. 减少迭代次数
