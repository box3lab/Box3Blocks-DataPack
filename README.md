# MC 神岛方块数据包

本数据包用于在 MC 神岛世界中统一管理方块相关的**合成配方**与**破坏掉落的战利品**。

## 数据包简介

- 使用 `block-id.json` 维护神岛方块 ID（带命名空间，如 `box3:grass`）。
- 在 `box3formula/data/box3/recipe/` 中维护方块合成配方 JSON 文件。
- 在 `box3formula/data/box3/loot_table/blocks/` 中维护方块破坏掉落 JSON 文件。

## 目录结构

```
box3project/
├── block-id.json                    # 方块 ID 与方块名映射
├── box3formula/
│   └── data/
│       └── box3/
│           ├── recipe/              # 合成配方
│           │   └── *.json
│           └── loot_table/
│               └── blocks/          # 方块战利品表
│                   └── *.json
├── check_blocks.py                  # 本地检查工具
├── CONTRIBUTING.md                  # 贡献指南
├── LICENSE                          # 许可证
├── .gitignore                       # Git 忽略文件
└── README.md                        # 本文件
```

## 许可证

本项目采用 [Apache License 2.0](LICENSE) 许可证。
