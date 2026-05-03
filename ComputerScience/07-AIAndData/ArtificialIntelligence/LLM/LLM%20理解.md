# LLM 理解

## 什么是 LLM
大语言模型 (Large Language Model) 是基于 Transformer 架构、海量文本预训练的深度学习模型。

## 核心能力
- **文本生成**：续写、翻译、摘要
- **理解与推理**：上下文理解、逻辑推理
- **代码生成**：多种编程语言
- **工具调用**：Function Calling

## 关键概念
- **Token**：模型处理的最小单位（≈0.75个英文词 / ≈1.5个中文词）
- **上下文窗口**：模型一次能处理的最大 Token 数
- **Temperature**：控制输出随机性（0=确定, 1=灵活）
- **Top-P**：核采样，只考虑累计概率 p 的 tokens
- **System Prompt**：设定模型行为的基础指令

## 模型架构
- Transformer (Attention is All You Need, 2017)
- GPT 系列 (OpenAI)
- Claude 系列 (Anthropic)
- DeepSeek (中国)
- Llama (Meta，开源)
