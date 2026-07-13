# 中文快速指南

## 适用范围

该Skill面向需要形成测试产物的理工科科研任务，包括科学计算、模型或方法对比、物理实验、观测数据分析、参数扫描、敏感性研究和科研流程复盘。

一次性计算、只需解释概念且不生成测试产物的任务不需要启用完整流程。

## 使用原则

- 先阅读项目级约束和已有证据，再设计测试。
- 缺失信息会改变比较对象、数据含义、对齐方式、指标、结论或操作权限时，停止执行并询问用户。
- 不修改原始输入，不擅自删除重要文件，不擅自安装依赖或修改conda、venv等环境。
- 每项非简单测试固定保留`task_plan.md`、`findings.md`和`progress.md`。
- 结果必须保留生成脚本和配置，不能只交付最终表格或图片。
- 运行成功与科学规律成立是两个独立结论。
- 用户没有提供验收阈值时，只报告描述性结果，不自行判断优劣或合格性。

## 三档流程

### Compact

适合少量输入、单个分析脚本、小型输出和无需高成本求解器的测试。至少保留三份规划文件、`test_spec.md`、README、最终结果和验证记录。

### Standard

适合多阶段、多case、包含中间结果或图表的测试。使用完整目录结构，分别保留准备、执行、分析、绘图和验证阶段。

### Extended

适合昂贵计算、物理实验、大数据、断点续算、并行任务、敏感输入或面向公开发表的结果。在Standard基础上增加环境快照、完整指纹、运行manifest、独立复算和发布审计。

## 标准工作流

### 建立测试合同

在`test_spec.md`中明确：

- 研究问题和可检验预期；
- 被测对象、参考对象和基线；
- 自变量、控制变量、测量变量和派生量；
- 单位、坐标或索引顺序、分组语义、符号和归一化规则；
- 权威输入、版本与溯源；
- 预处理、对齐、映射、插值、聚合和加权方式；
- 主指标、边界情况和验收阈值；
- case、重复、随机种子和失败处理；
- 预期产物、资源消耗和执行授权。

### 建立独立工作区

编辑`scripts/init_test_workspace.py`顶部配置区后运行。默认工作区职责如下：

```text
test_workspace/
├── task_plan.md
├── findings.md
├── progress.md
├── test_spec.md
├── README.md
├── inputs/
├── config/
├── scripts/
├── intermediate/
├── results/
├── figures/
├── logs/
├── records/
└── report/
```

输入、脚本、中间结果、最终结果、图表、日志和验证记录不得混放。测试编号或日期命名方式应服从目标项目已有规范。

### 建立可追踪执行链

准备、运行、分析、绘图和验证具有不同失败模式时，使用独立阶段脚本。每个阶段应检查输入，记录实际配置、时间、状态和日志，只向测试工作区写入产物。

断点复用必须比较输入、代码、模型或校准、配置和相关环境的完整指纹。文件存在、行数正确或时间戳较新不足以证明产物可以安全复用。

### 独立验证

验证至少覆盖：

- 文件、schema、行数、键、单位和有限值；
- 输入与配置指纹；
- 坐标、索引、通道和分组对齐；
- 守恒、边界、范围、单调性或其他领域不变量；
- 从更低层产物独立复算部分指标；
- 表格、JSON、CSV、图表和文字结论一致；
- README命令、路径和产物说明与实际目录一致。

验证报告必须分别写明运行完整性状态和科学验收状态。科学状态可为PASS、FAIL或NOT_DEFINED。

### 管理和发布产物

根据产物用途标记`publish`、`local-only`、`regenerate`或`exclude`。大文件应说明保留、外部存储、重新生成或经同意删除的策略。

发布前运行：

- `build_artifact_manifest.py`
- `validate_test_workspace.py`
- `audit_publishability.py`

这些脚本仅报告和验证，不会自动清理用户文件。

## 文档与科研写作

README面向复现人员，可以写明文件、脚本、命令、环境、输入输出和运行限制。

科研报告面向目标读者，不暴露对话、用户指令、修改过程、本地绝对路径和后台脚本位置。正文只写有证据支撑的内容。涉及公式时，给出公式，并在下一行以“其中，……”说明所有字母和符号。

完整英文规范见：

- [workflow-and-gates.md](workflow-and-gates.md)
- [scenario-branches.md](scenario-branches.md)
- [provenance-and-artifacts.md](provenance-and-artifacts.md)
- [verification-and-acceptance.md](verification-and-acceptance.md)
- [scientific-writing.md](scientific-writing.md)
