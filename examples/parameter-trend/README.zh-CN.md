# 参数趋势证据包示例

[English](README.md) | [简体中文](README.zh-CN.md)

该完整示例用于检验4个有序参数取值下，测量响应是否严格递增。

## 状态

- 运行完整性验证：PASS
- 科学验收：PASS
- 验收条件：所有相邻响应差均大于0

## 证据包

| 位置 | 职责 |
|---|---|
| `inputs/measurements.csv` | 不可变的4个case输入样例 |
| `test_spec.md` | 研究问题、数据语义、指标和验收条件 |
| `scripts/analyze_and_verify.py` | 分析、独立复算和运行记录生成 |
| `results/trend_summary.csv` | 机器可读最终指标 |
| `evidence_ledger.md` | 连接验证证据与科学结论 |
| `records/` | 工作区合同、运行记录、产物manifest和验证记录 |

## 复现方法

在本目录运行：

```bash
python scripts/analyze_and_verify.py
python ../../skill/build-reproducible-research-tests/scripts/build_artifact_manifest.py
python ../../skill/build-reproducible-research-tests/scripts/validate_test_workspace.py
```

第一个脚本只允许覆盖其声明的生成产物：`results/trend_summary.csv`、`records/run_record.json`和`records/verification_report.md`。输入、测试规范和证据台账保持不变。
