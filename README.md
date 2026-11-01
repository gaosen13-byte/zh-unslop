# zh-unslop

给 Codex 和 Claude Code 用的中文去 AI 腔写作 Skill：保留原意，把话写得自然、直接、具体。

**改前：**“随着技术不断发展，我们全面提升了服务体验。让我们开启全新旅程！”  
**改后：**“新版本把首页加载时间从 4 秒降到 1 秒。现在可以在订单页直接申请退款。”

## 安装

把仓库中的 `SKILL.md` 放进对应的 skills 目录：

- Codex：`~/.codex/skills/zh-unslop/SKILL.md`
- Claude Code：`~/.claude/skills/zh-unslop/SKILL.md`

可以克隆后复制：

```sh
git clone https://github.com/gaosen13-byte/zh-unslop.git
mkdir -p ~/.codex/skills/zh-unslop
cp zh-unslop/SKILL.md ~/.codex/skills/zh-unslop/SKILL.md
# Claude Code 使用时改为 ~/.claude/skills/zh-unslop
```

## 检查文本

`check.py` 仅依赖 Python 标准库。传入 UTF-8 文本文件，或从标准输入读取：

```sh
python3 check.py examples/01-product.md
cat draft.txt | python3 check.py
```

脚本会列出命中的句子及原因，并给出 0–100 的启发式“AI 味”分。分数按命中项累计，最高 100；它用于提醒常见表达，不代表对文本来源的判断。

## 示例

[`examples/`](examples/) 有两组改写对照。检查改写后的文本：

```sh
python3 check.py examples/clean.txt
```

## 许可

[MIT](LICENSE)
