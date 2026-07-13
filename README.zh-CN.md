# 可复现科研测试Skill

[English](README.md) | [简体中文](README.zh-CN.md)

这是一个可独立运行的Codex Skill，用于设计、执行、验证、记录和封装可复现的理工科科研测试。

适用场景包括科学计算对比、仿真与模型验证、物理实验、观测数据分析、参数扫描、敏感性研究以及既有科研测试流程审查。Skill将科研问题转化为可审计的测试包，建立原始输入、配置、执行记录、中间变换、最终结果、图表、验证证据和科学结论之间的追踪关系。

## 核心能力

- 为每项测试建立职责明确的独立工作区。
- 固定使用`task_plan.md`、`findings.md`和`progress.md`持续记录计划、证据、决策、异常和进度。
- 在高成本计算、实验或状态变更操作前建立测试合同和执行门。
- 明确区分已确认事实、拟议方案、待确认问题和科学解释。
- 根据任务规模提供Compact、Standard和Extended三档流程。
- 提供计算、物理实验、观测研究、参数扫描、方法比较和科研可视化分支。
- 将运行完整性验证与科学验收结论分开管理。
- 保留生成脚本、配置、日志、manifest、校验和与独立验证记录。
- 区分技术复现README和面向目标读者的科研报告。
- 在发布前检查缓存、大文件、绝对路径、疑似敏感信息和不适合发布的产物，检查工具不会自动删除文件。

该Skill不依赖planning-with-files、绘图Skill、MCP服务器或第三方Python包。配套工具仅使用Python标准库。

## 仓库结构

```text
.
├── README.md
├── README.zh-CN.md
├── LICENSE
├── skill/
│   └── build-reproducible-research-tests/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── assets/workspace-template/
│       ├── references/
│       └── scripts/
└── examples/
    └── compact-parameter-trend/
```

仓库级README和许可证位于Skill目录之外，Skill本体保持标准目录结构，可以单独复制和安装。

## 安装

将Skill目录复制到Codex Skills目录：

```bash
cp -R skill/build-reproducible-research-tests "$CODEX_HOME/skills/"
```

随后显式调用：

```text
$build-reproducible-research-tests
```

示例请求：

```text
使用$build-reproducible-research-tests设计两种数值方法的可复现对比测试。先制定计划，识别缺失的科学决策，获得确认后再开始执行。
```

Skill内部的[中文快速指南](skill/build-reproducible-research-tests/references/quickstart-zh-CN.md)说明了标准工作流、目录职责、三档裁剪方式和完成检查。

## 配套工具

所有脚本都在文件顶部提供集中配置区，不使用命令行参数。运行前应先检查并修改配置区。

| 脚本 | 作用 |
|---|---|
| `init_test_workspace.py` | 从模板非破坏性地创建科研测试工作区 |
| `capture_environment.py` | 记录环境事实，不安装或修改环境 |
| `build_artifact_manifest.py` | 清点产物并以流式方式计算SHA-256 |
| `validate_test_workspace.py` | 检查目录、占位符、JSON记录和manifest一致性 |
| `audit_publishability.py` | 报告缓存、大文件、本机路径和疑似敏感内容 |

这些工具负责通用结构和溯源检查。每项科研测试仍需根据研究对象实现领域语义检查和独立数值验证。

## 完整示例

[`examples/compact-parameter-trend`](examples/compact-parameter-trend/README.zh-CN.md)提供一个小型、完整、可复现的参数趋势测试。示例包含不可变输入、全局变量风格分析脚本、机器可读结果、验证报告和三份持续规划文件。

在示例目录运行：

```bash
python scripts/analyze_and_verify.py
```

## 安全边界

该流程不会自行授权安装依赖、修改环境、删除重要文件、覆盖原始输入、对外发布或形成缺乏证据的科学结论。会改变测试含义的缺失信息必须在执行前向用户确认。自动发布检查只报告风险，不删除或改写用户文件。

## 验证状态

Skill已通过官方结构校验。5个配套脚本已完成语法与功能测试，覆盖如下内容：

- 非破坏性工作区初始化；
- 拒绝未完成的模板；
- Compact、Standard和Extended三档工作区验证；
- 环境快照；
- 产物哈希与manifest一致性；
- 发布风险检查；
- 无阻塞项、无警告项的最终发布审计。

## 许可证

本项目采用[MIT License](LICENSE)。
