# Changelog

所有重要变更都会记录在此文件中。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

## [Unreleased]

- 更新.gitignore和添加CHANGELOG.md文件

## [2.1.0] - 2026-04-19

### 修复

- **任务执行器**：将线程池并发执行改回串行执行（使用锁），修复任务中断重连时的状态竞争问题
- **状态文件名**：修复 `SUMMARIZING` 阶段状态文件命名错误（`task_id_markdown.status.json` → `task_id.status.json`）
- **日志输出**：移除视频帧提取时的调试打印语句（`2#3` 等）
- **测试类命名**：修正 `TestConcurrentTaskExecutor` → `TestSerialTaskExecutor`

### 优化

- **转写器初始化**：增强初始化逻辑，支持 `model_size` 和 `device` 参数传递
- **Chat 服务**：优化 MiniMax 的 `reasoning_split` 处理逻辑
- **模型服务**：改进获取模型失败时的错误处理
- **OpenAI 兼容提供商**：加强连通性测试稳定性

### 配置

- 添加 `.graphifyignore` 配置，排除生成内容（视频帧、笔记结果等）不纳入代码图谱
- 更新 `.env.example` 中的 API 端口配置
- 更新 `run.bat` 使用 venv 和 pnpm
