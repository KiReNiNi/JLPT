# 橘园 N1

N1 真题刷题网站。现在收录 2026 年 7 月的言語知識（問題1–7，共 44 题）。

## 文件

| 路径 | 作用 |
|---|---|
| `build/q2026.py` | 2026.7 的题目、答案、中文翻译和解析（手工录入） |
| `build/build.py` | 用 janome 切词，生成 `build/data.json` |
| `build/template.html` | 页面本体：CSS、HTML 外壳和全部 JS。题目数据的位置写的是 `__DATA__` |
| `build/assemble.py` | 把 `data.json` 填进模板，生成 `site/index.html` |
| `site/index.html` | 生成出来的页面，不要直接改 |
| `site/bg/bg1–8.jpg` | 橘园主题的 8 张背景图（720×1280）。生成页面时会转成 data URI 嵌进 `index.html`，因为 Artifact 页面里按相对路径引用的图片加载不出来 |

重新生成页面：

```
pip install janome
python3 build/build.py
python3 build/assemble.py
```

## 美化页面时请遵守

页面发布成 claude.ai 的 Artifact。做题记录存在 Artifact 自带的云端数据库里（`window.claude.use("db")`），所以：

1. **只改 `build/template.html` 的 `<style>` 部分和图片**。本轮按用户要求，只给皮肤背景选择增加了按页面稳定分配及 `render()` 的背景刷新调用，不属于学习逻辑重构。其他 JS 里的数据读写、`data-act` 属性、`data-k` / `data-q` / `data-n` 等属性都不要动，改了会坏功能或丢记录。
2. 颜色都写成 `:root` 里的变量（`--accent`、`--card` 等），橘园主题的变量在 `body[data-skin="orchard"]` 里。改配色优先改变量。
3. **不能用内联 `style="..."` 属性**，页面运行环境会拦掉。宽度和背景图需要动态设置的，用 `data-w` / `data-bgi`，由 JS 的 `paint()` 设置。换背景图就替换 `site/bg/` 里的文件（保持 bg1.jpg…的命名），不要在 CSS 里写 `url("bg/...")`，那样在网站上显示不出来。
4. 外部资源只能来自：cdnjs.cloudflare.com、cdn.jsdelivr.net、unpkg.com（脚本），fonts.googleapis.com（字体）。图标直接写成内联 SVG；新加的图片要像背景图一样在 `assemble.py` 里转成 data URI，不能按文件路径引用。
5. 要在手机宽度（约 390px）下正常显示，不能出现横向滚动。
6. 改完提交回这个仓库就行，由 Claude 重新生成并发布到原来的网址，记录不会丢。

## 页面结构（class 名）

- 顶栏 `.top`：返回 `.ibtn`、标题 `.ttl`、同步状态 `.cloud`、模式切换 `.mode`（`.a` 选答案 / `.k` 标生词）
- 首页：`.hero`、`.resume`（继续上次）、`.btn.pri`（开始做题）、`.tiles`/`.tile`（备用、暂存生词、单词本）、`.papers`/`.paper`（套卷列表，含进度条 `.bar`）
- 套卷题库：`.tabs`（单词/阅读/听力）、`.filters`/`.flt`（全部 / 暂时备用 / 过了 / 上次错，可点击筛选）、`.grp`（题型分组）、`.qc`（单题卡片，`.hold` 备用黄底、`.pass` 过了粗框、`.dot` 上次错红点）
- 题目卡 `.card.qcard`：`.qhead`（题号标签 + 小眼睛 `.peek`）、`.stem` 题干、`.opts`/`.op` 选项（`.pick` 选中蓝、`.right` 正解、`.wrong` 选错）、排序题 `.sortline`/`.slot`/`.chips`/`.chip`、解析 `.exp`、备用/过 `.acts`/`.act`
- 标生词：`.marking .tk`（可点的词）、`.tk.on`（已标绿）、`.op.whole`/`.chip.whole`（整个选项标绿）、工具条 `.markbar`（隐藏 / 数量 / 撤销 / 保存）
- 备注 `.note`：可收起，`.note-ok` 是保存按钮
- 底栏 `.foot`：上一题 / 下一题 `.btn`，题号格子 `.dots`
- 选题 `.fs`/`.ch`/`.stepper`、结果 `.score`/`.rrow`、单词 `.wd`、外观弹层 `.sheet`/`.bgs`

## 2026-11-12：背景遮挡修复（交回 Claude 发布）

- 橘园皮肤去掉顶部吸顶毛玻璃、卡片背景模糊以及整张插画上的白粉渐变；保留原按钮、卡片底色、圆角、题库和交互。
- “每页随机”在本次打开期间给首页、套卷、单题、选题、做题、结果、生词本分配互不相同的原背景，返回与数据刷新保持稳定。使用独立的图片随机数，不干扰出题随机数。
- 手动选择某张背景仍表示全站固定使用它；原来固定选图的偏好不会被强制改掉。想按页面换图，在外观中选择“每页随机”。
- 八张JPEG和 data URI 嵌入方式不变；不恢复失效的相对图片路径。题库、数据库路径/字段、答案判分、备注、生词读写和全部事件属性不变。
- `site/index.html` 已重新生成并提交，可交回 Claude 在原 Artifact 更新；本轮没有另外创建网址或自行发布。
- 边界检查：`node tests/orchard-boundary.cjs`。浏览器检查：`JLPT_ENGINE=chromium node tests/orchard-browser.cjs`，WebKit用`JLPT_ENGINE=webkit`。所有数据库操作均为隔离模拟，详见 [交接与截图](docs/ORCHARD-BACKGROUND-FIX.md)。
