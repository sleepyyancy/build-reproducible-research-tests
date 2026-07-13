# Compact参数趋势测试示例

[English](README.md) | [简体中文](README.zh-CN.md)

该完整示例用于检验4个有序参数取值下，测量响应是否严格递增。

## 复现方法

在本示例目录运行：

```bash
python scripts/analyze_and_verify.py
```

脚本会检查输入列、标识符唯一性、数值有限性和参数顺序，随后重新生成：

- `results/trend_summary.csv`
- `records/verification_report.md`

这两个文件被明确标记为脚本生成产物，允许由该脚本重新生成。脚本不会修改输入文件和规划文档。

## 测试状态

- 运行完整性验证：PASS
- 科学验收：PASS
- 验收条件：所有相邻响应差均大于0
