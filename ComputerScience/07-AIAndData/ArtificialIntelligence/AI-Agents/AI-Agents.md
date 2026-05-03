# AI Agents

## 什么是 Agent
Agent 是具有**自主决策能力**的 AI 系统，它能感知环境、制定计划、调用工具、执行任务。

### 核心要素
1. **感知 (Perception)**：获取信息
2. **推理 (Reasoning)**：制定计划
3. **行动 (Action)**：调用工具执行
4. **记忆 (Memory)**：短期/长期记忆
5. **反馈 (Feedback)**：根据结果调整

## 单 Agent vs 多 Agent

| 类型 | 场景 | 典型架构 |
|------|------|---------|
| 单 Agent | 明确任务 | ReAct, Plan-and-Execute |
| 多 Agent | 复杂协作 | 监督者-工作者、辩论、市场 |

## 工具使用设计模式
- **Function Calling**：LLM 输出 JSON 调用函数
- **MCP (Model Context Protocol)**：标准化工具接入协议
- **A2A (Agent-to-Agent)**：Agent 间通信协议

## 关键概念
- **Agentic RAG**：普通 RAG + Agent 决定搜索策略
- **上下文工程**：不是提示词工程，而是 context 组织
- **可观测性**：Agent 执行的 trace、log、eval
