# 贡献指南

欢迎为 MC 神岛方块数据包贡献配方和战利品表！请按照以下步骤进行，确保协作顺畅。

## 新增方块的完整流程

### 1. 查看神岛方块 ID

- `block-id.json` 是只读文件，包含神岛模组提供的所有方块 ID。
- 打开 `block-id.json` 查看可用的方块 ID。
- 选择你要添加配方的方块，记录其方块名（如 `box3:grass`）。

**注意**：不要修改 `block-id.json`，它仅用于获取神岛模组提供的方块 ID。

### 2. 创建配方文件

#### 方式一：可视化编辑（推荐）

- 使用在线配方编辑器：https://crafting.thedungeone7i0n.ca/
- **配置选项**：在编辑器中设置 `Minecraft Version` 为 `Java 1.21.11`。
- 在编辑器中拖拽设计配方，导出 JSON。
- **重要**：导出的 JSON 使用原版方块 ID，你需要手动替换为神岛方块 ID（带 `box3:` 前缀）。
- 将修改后的 JSON 保存到 `box3formula/data/box3/recipe/` 目录，文件名去掉命名空间。

#### 方式二：手动编写

- 在 `box3formula/data/box3/recipe/` 目录下新建 JSON 文件。
- 文件名应为 **去掉命名空间** 的方块名，例如 `grass.json`。
- 按照标准 Minecraft 配方格式编写内容。
- Wiki：https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9

示例路径：

```
box3formula/data/box3/recipe/grass.json
```

### 3. 创建战利品表（方块破坏掉落）

- 在 `box3formula/data/box3/loot_table/blocks/` 目录下新建 JSON 文件。
- 文件名同样去掉命名空间，例如 `grass.json`。
- 按照标准 Minecraft 战利品表格式编写内容。
- Wiki：https://zh.minecraft.wiki/w/%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8

示例路径：

```
box3formula/data/box3/loot_table/blocks/grass.json
```

### 4. 运行本地检查工具

在项目根目录下运行：

```bash
python3 check_blocks.py
```

- 检查 `block_check_report.md`，确认：
  - 新增的方块没有出现在"缺失"列表中。
  - 没有多余的文件出现在报告里。

### 5. 提交代码

- 提交前请确保本地检查报告无异常。
- 提交信息建议包含新增/修改的方块信息，例如：
  ```
  feat: add grass block recipe and loot table
  ```

## 命名规范

- **方块 ID**：`box3:snake_case_name`（小写+下划线）。
- **文件名**：去掉命名空间，如 `snake_case_name.json`。
- **JSON 内容**：遵循 Minecraft 官方格式。

## 测试要求

1. **安装数据包**：
   - 将整个项目克隆到你的世界存档的 `datapacks` 目录中。
   - 路径示例：`.minecraft/saves/你的世界名/datapacks/`
   - Minecraft 会自动读取 `box3formula` 文件夹作为数据包。
     ![](https://cdn-community.bcmcdn.com/47/community/A7GBBjeZ9DYuPoRf4FT1UVwbOssD6Ia63ChxbAscwcxe.png?hash=Fln_Za5ISvi4Q3vVu6DPE6KKSEVK)

2. **游戏内测试**：
   - 进入世界后，数据包会自动加载。
   - 测试新增的配方是否可以在合成台中使用。
   - 测试破坏方块时是否有正确的掉落物。

3. **验证加载**：
   - 在游戏中输入 `/reload` 重新加载数据包。
   - 使用 `/datapack list` 查看数据包是否已启用。

- **检查工具**：提交前务必运行 `python3 check_blocks.py`，无异常再提交。

## 提交规范

- **分支**：请基于 `main` 分支创建新分支进行开发。
- **Commit 消息**：使用语义化格式，如 `feat:`、`fix:`、`docs:` 等。
- **PR 说明**：简要说明修改内容，必要时附上游戏内截图或测试说明。

## 代码审查

- 审查重点包括：
  - 命名规范
  - JSON 格式正确性
  - 本地检查报告无异常
  - 游戏内测试结果

## 联系方式

如有疑问，请：

- 在仓库中新建 Issue。
- 或联系项目维护者。

感谢你的贡献！ 🎉
