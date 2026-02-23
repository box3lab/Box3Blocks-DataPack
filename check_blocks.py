"""MC 神岛方块资源检查脚本

用途：
    - 基于 ``block-id.json`` 中记录的方块名，检查 datapack 中是否存在对应的：
        * 合成配方：``<PROJECT_ID>/data/<MOD_ID>/recipe/*.json``
        * 方块战利品表：``<PROJECT_ID>/data/<MOD_ID>/loot_table/blocks/*.json``
    - 自动生成 ``block_check_report.md``，给配方贡献者查看进度用。

本脚本会做什么：
    - 检查是否有 **缺少的方块文件**（在 ``block-id.json`` 里有名字，但没有对应的 recipe / loot_table 文件）。
    - 检查是否有 **多余的方块文件**（有 recipe / loot_table 文件，但文件名不在 ``block-id.json`` 中）。
    - 在 Markdown 报告中按“完成情况”排序方块：已完成的排在最前面。

本脚本不会做什么：
    - 不会检查 JSON 内容是否合法或是否符合游戏逻辑。
    - 不会在游戏内做任何自动测试或生成方块，仅做**静态文件存在性检查**。
    - 因此，所有配方 / 掉落效果仍然需要贡献者在游戏中自行测试验证。

如何使用：
    1. 在该目录下运行：::
           python3 check_blocks.py
    2. 查看生成的 ``block_check_report.md``，确认哪些方块已完成 / 缺失 / 多余。

Python 版本要求：
    - 推荐 **Python 3.9+**。

提交前检查：
    - 每次将 datapack 提交到远程仓库之前。
    - 每次拉取代码时，检查方块是否被其他贡献者贡献，是否有缺失或多余的方块文件。
"""

import json
from pathlib import Path

PROJECT_ID = "box3formula"
MOD_ID = "box3"

# ====== 使用当前脚本所在目录作为基准路径 ======
BASE_DIR = Path(__file__).resolve().parent

BLOCK_ID_JSON = BASE_DIR / "block_id.json"

RECIPE_DIR = BASE_DIR / PROJECT_ID / "data" / MOD_ID / "recipe"

LOOT_TABLE_BLOCKS_DIR = BASE_DIR / PROJECT_ID / "data" / MOD_ID / "loot_table" / "blocks"
# ============================================================


def load_block_names_from_block_id(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    raw_names = set(data.values())

    # 去掉前缀，例如 "box3:grass" -> "grass"，方便和文件名对齐
    prefix = f"{MOD_ID}:"
    names: set[str] = set()
    for name in raw_names:
        if isinstance(name, str) and name.startswith(prefix):
            names.add(name[len(prefix) :])
        else:
            names.add(name)

    return names


def list_json_basenames(directory: Path) -> set[str]:
    if not directory.exists():
        print(f"[警告] 目录不存在: {directory}")
        return set()

    names = set()
    for entry in directory.iterdir():
        if entry.is_file() and entry.suffix == ".json":
            names.add(entry.stem) 
    return names


def index_block_files(block_names: set[str], directory: Path) -> tuple[dict[str, set[str]], list[str]]:
    if not directory.exists():
        print(f"[警告] 目录不存在: {directory}")
        return {name: set() for name in block_names}, []

    block_to_files: dict[str, set[str]] = {name: set() for name in block_names}
    extra_files: list[str] = []

    stems: list[str] = []
    for entry in directory.iterdir():
        if entry.is_file() and entry.suffix == ".json":
            stems.append(entry.stem)

    for stem in stems:
        best_block: str | None = None
        for block in block_names:
            if stem == block or stem.startswith(block + "_"):
                if best_block is None or len(block) > len(best_block):
                    best_block = block

        if best_block is not None:
            block_to_files.setdefault(best_block, set()).add(stem)
        else:
            extra_files.append(stem)

    return block_to_files, extra_files


def write_markdown_report(
    block_names: set[str],
    recipe_map: dict[str, set[str]],
    loot_map: dict[str, set[str]],
    total_recipe_files: int,
    total_loot_files: int,
    extra_recipe: list[str],
    extra_loot: list[str],
) -> None:
    report_path = BASE_DIR / "block_check_report.md"

    lines: list[str] = []
    # 方块检查报告
    lines.append("# 方块检查报告")
    lines.append("")
    lines.append(f"- 总方块数量：{len(block_names)}")
    lines.append(f"- recipe 文件数：{total_recipe_files}")
    lines.append(f"- loot_table/blocks 文件数：{total_loot_files}")
    lines.append("")

    # 总览表
    lines.append("## 方块完成情况总览")
    lines.append("")
    lines.append("| 方块名 | 合成配方 | 破坏掉落 |")
    lines.append("| ------ | -------- | -------- |")

    # 排序：优先显示 recipe 和 loot 都完成的方块，然后再显示有缺失的
    def sort_key(block_name: str) -> tuple[int, int, str]:
        recipe_count = len(recipe_map.get(block_name, set()))
        loot_count = len(loot_map.get(block_name, set()))
        recipe_flag = 0 if recipe_count > 0 else 1
        loot_flag = 0 if loot_count > 0 else 1
        return (recipe_flag + loot_flag, recipe_flag, loot_flag, block_name)

    for name in sorted(block_names, key=sort_key):
        recipe_count = len(recipe_map.get(name, set()))
        loot_count = len(loot_map.get(name, set()))
        has_recipe = "❌" if recipe_count == 0 else f"🎉 x{recipe_count}"
        has_loot = "❌" if loot_count == 0 else f"🎉 x{loot_count}"
        lines.append(f"| {name} | {has_recipe} | {has_loot} |")

    # 多余文件
    lines.append("")
    lines.append("## 目录中多余的文件")

    lines.append("")
    lines.append("### 合成配方（recipe）目录中多余的文件")
    if extra_recipe:
        lines.append("")
        for name in extra_recipe:
            lines.append(f"- {name}.json")
    else:
        lines.append("")
        lines.append("- 无")

    lines.append("")
    lines.append("### 方块战利品表（loot_table/blocks）目录中多余的文件")
    if extra_loot:
        lines.append("")
        for name in extra_loot:
            lines.append(f"- {name}.json")
    else:
        lines.append("")
        lines.append("- 无")

    report_text = "\n".join(lines) + "\n"
    with report_path.open("w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\n[信息] 已生成 Markdown 报告: {report_path}")


def main():
    # 1. 读取 block-id.json 的方块名
    if not BLOCK_ID_JSON.exists():
        print(f"[错误] 找不到 block-id.json: {BLOCK_ID_JSON}")
        return

    block_names = load_block_names_from_block_id(BLOCK_ID_JSON)
    print(f"从 block-id.json 读取到 {len(block_names)} 个方块")

    # 2. 读取并按方块名归类 recipe 目录的文件
    recipe_map, extra_recipe = index_block_files(block_names, RECIPE_DIR)
    total_recipe_files = sum(len(v) for v in recipe_map.values()) + len(extra_recipe)
    print(f"\nrecipe 目录中找到 {total_recipe_files} 个 json 文件")

    # 3. 读取并按方块名归类 loot_table/blocks 目录的文件
    loot_map, extra_loot = index_block_files(block_names, LOOT_TABLE_BLOCKS_DIR)
    total_loot_files = sum(len(v) for v in loot_map.values()) + len(extra_loot)
    print(f"\nloot_table/blocks 目录中找到 {total_loot_files} 个 json 文件")

    # 4. 写入 Markdown 报告
    write_markdown_report(
        block_names=block_names,
        recipe_map=recipe_map,
        loot_map=loot_map,
        total_recipe_files=total_recipe_files,
        total_loot_files=total_loot_files,
        extra_recipe=extra_recipe,
        extra_loot=extra_loot,
    )

    print("\n========= 检查完成 =========")


if __name__ == "__main__":
    main()