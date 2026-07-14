# 可复现科研测试Skill

[English](README.md) | [简体中文](README.zh-CN.md)

这是一个可独立运行的Codex Skill，用于把多阶段理工科科研测试组织成可审计证据链。

适用场景包括科学计算对比、仿真与模型验证、物理实验、观测数据分析、参数扫描、敏感性研究和方法基准测试。概念解释、只读结果摘要、一次性计算、普通代码修改和单独画图不会被扩展成繁重的测试包。

## 证据链

```text
源数据身份→测试规范→冻结设置→运行记录
→派生产物→机器可读结果→独立验证
→证据台账→科学结论
```

主要能力包括：

- 明确研究问题、权威状态、数据语义、指标、边界情况、阈值和排除结论。
- 保存输入身份、影响结果的实际设置、运行状态、终止证据和产物来源。
- 分开记录运行完整性验证和科学验收结论。
- 从低层产物独立复算部分数值，或检查独立科学不变量。
- 通过证据台账把每项实质性结论连接到经过验证的证据。
- 保留结果生成和验证入口，避免只留下无法复现的最终文件。
- 仅在科学主张确有需要时增加哈希、环境记录、日志、中间结果、断点指纹和发布控制。
- 区分技术复现README与面向目标读者的科研报告。
- 发布前检查缓存、大文件、绝对路径和疑似敏感信息，检查工具不会删除文件。

配套工具仅使用Python标准库。

## 最小证据包

```text
test_workspace/
├── README.md
├── test_spec.md
├── evidence_ledger.md
├── scripts/
├── results/
└── records/
```

根据测试实际需要增加`inputs/`、`config/`、`intermediate/`、`figures/`、`logs/`和`report/`。初始化器会把声明结构写入`records/workspace_contract.json`，验证器按照合同检查，不会因为缺少无关空目录而判定失败。

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
    └── parameter-trend/
```

仓库文档、许可证和完整示例位于Skill目录之外，Skill本体可以独立安装。

## 安装

使用Codex Skill安装器从本仓库安装：

- 仓库：`sleepyyancy/build-reproducible-research-tests`
- 路径：`skill/build-reproducible-research-tests`

安装后调用：

```text
$build-reproducible-research-tests
```

示例请求：

```text
使用$build-reproducible-research-tests为两种数值方法建立可审计对比测试包，保留已标识输入、机器可读结果、独立验证和证据支持的结论。
```

## 配套工具

运行前编辑脚本顶部配置区。

| 脚本 | 作用 |
|---|---|
| `init_test_workspace.py` | 创建最小证据包，并只创建本测试声明需要的可选组件 |
| `capture_environment.py` | 只读记录影响复现的环境事实 |
| `build_artifact_manifest.py` | 清点产物并以流式方式计算SHA-256 |
| `validate_test_workspace.py` | 检查合同声明产物、非空核心职责、JSON记录、占位符和manifest身份 |
| `audit_publishability.py` | 报告缓存、大文件、本机路径和疑似敏感内容 |

这些工具负责结构和溯源检查。每项科研测试仍需实现与科学主张相匹配的领域语义检查和独立数值验证。

## 完整示例

[`examples/parameter-trend`](examples/parameter-trend/README.zh-CN.md)用于检验4个有序参数取值下测量响应是否严格递增。示例包含不可变输入、明确的测试规范、证据台账、运行记录、机器可读结果、指标独立复算、产物manifest和验证报告。

在示例目录运行：

```bash
python scripts/analyze_and_verify.py
```

## 验证状态

Skill已通过官方结构校验。5个配套脚本已通过语法和功能检查，覆盖：

- 不创建无关可选目录的最小初始化；
- 只创建声明组件的选择性初始化；
- 拒绝覆盖已有测试包；
- 环境事实采集；
- 产物哈希与manifest一致性；
- 按合同动态验证工作区；
- 发布风险检查；
- Markdown本地链接和包内一致性检查。

## 许可证

本项目采用[MIT License](LICENSE)。
