# 粉樱花园 / 森林水晶：布局更新与交接

2026-11-12。基线 `cd1a971b88ee1d3e38c81cd710ab0f9cef9ee87d`。本轮由用户明确要求调整整个网站布局、换掉橙色大按钮，并验证真实手机宽度下的图片与进入练习换景行为。

**交回原分支 `claude/tender-hopper-moneok`；没有另建网站，没有发布到原 Artifact，没有访问或更改真实学习数据库。**

## 当前设计

- 首页改为标题、练习区、学习记录、套卷目录。大块橙色按钮改成浅色渐变磨砂入口；套卷目录放在同一张卡片内，减少重复的大胶囊。
- 粉色采用玫瑰灰、米白、细边框；新增森林绿色皮肤，沿用用户此前言叶小岛的原森林水晶插画。简洁皮肤保留。标题采用宋体，日文题干仍使用原来的可读字体。
- 套卷的筛选改为手机两列，四个状态完整显示；题型分组增加小序号。选题区、题目、结果、生词、备注与外观面板统一间距、边框与配色。
- 去掉全屏遮图渐变和顶部吸顶模糊。用户本轮要求的磨砂仅用于卡片和按钮，背景插画本身清晰。
- 外观面板提供粉樱花园 / 森林水晶 / 简洁，缩略图完整显示。没有生成新图片或改动原图像素。

## 图片与壁纸行为

以前手动选择某张图片会固定全站，因此即便点“开始做题”，图片也不变。本轮有意改变这个展示行为：选图只固定首页；进入选题、进入答题会换景，每次新建练习轮次也会换图。同一轮内选答案、输入备注、云端刷新不会重新随机图片。

粉色原八张 JPEG 保持字节不变。新增四张森林 JPEG 从此前言叶小岛 `public/wallpapers/` 原图复制，文件名为 `crystal`、`valley`、`books`、`blossom`。`assemble.py` 将十二张图全部转成 data URI 嵌进 HTML，避免 Artifact 无法访问 `bg/xxx.jpg` 的问题。森林只有四张图，不承诺七种页面各用一张不同图片；首页→选题→答题的三个阶段使用不同图片。

最终 HTML 约 2.78 MB。没有引入图片服务器或新的存储服务。图片 SHA-256、模板与发布 HTML 哈希见 [源码核对结果](garden-layout/source-check.json)。

## 数据保护与备份

- 云端存储仍为 `window.claude.use('db')`。`progress/<question-id>`、`words/<doc-id>`、`sessions/current`、`settings/main` 路径及字段未变。
- 44 道题、题目 ID、答案、解析、切词数据、全部事件处理、判分、备注和生词保存代码与基线做逐字节比对，保持不变。
- 改动的 JS 为展示模板、外观面板、图片池及换景逻辑；没有数据库迁移或数据清理。
- 原版源码和素材备份：`backup/orchard-original-images-f7d341b`、`backup/orchard-before-clear-dcf3f44`；布局更新前的完整版本：`backup/orchard-before-layout-cd1a971`。
- 没有操作真实云端学习数据，因此 Git 备份包含源码和素材，**不等于真实学习数据库备份**。

## 检查范围

实际运行 Chromium 与 WebKit，在 390px 和 430px 手机视口、触摸模式和 2 倍像素密度下检查。这里是浏览器手机模拟，不是真 iPhone。测试宿主提供与 Artifact 嵌入页相同用途的 viewport 元信息。

- 粉色、绿色的首页、选题、答题、结果、套卷、单题、生词和外观面板均截图。
- 固定首页图片时，实际点击练习入口和开始按钮，验证背景数据的哈希改变；开启第二轮再次改变；同一轮连续十次刷新不变。
- 十二张内嵌图片全部解码成功，画廊图片数量与对应皮肤一致。
- 两种皮肤分别渲染全部 44 道题检查横向溢出。
- 实际点击答案、提交、保存备注、切换状态、标记生词、保存、重新加载；隔离存储中的记录保留。预先注入的旧记录及旧单词逐字段保持一致。
- 简洁皮肤能隐藏壁纸，切回森林及重新加载后偏好仍存在。无页面 JS 异常。
- 测试读取真实字体服务，没有用空白 CSS 代替字体。加载情况写入机器报告。
- 截图逐项查看了背景、卡片、文字、按钮和外观缩略图；本地测试范围内未发现黑屏、蓝色问号、图片加载占位、花朵跨卡覆盖或横向溢出。

数据库使用 Node 内存 Map 模拟 Artifact API，隔离于正式数据。截图里的数量属于测试样本，不代表用户的学习进度。

机器报告：[Chromium](garden-layout/chromium/verification.json) / [WebKit](garden-layout/webkit/verification.json)。源码检查：`node tests/garden-layout-boundary.cjs`。浏览器：`JLPT_ENGINE=chromium node tests/garden-layout-browser.cjs` / `JLPT_ENGINE=webkit node tests/garden-layout-browser.cjs`。旧 orchard 测试入口转发到当前测试，旧实现可从基线提交读取。WebKit 的执行器默认使用当前环境的 `/tmp/jlpt-webkit-run.sh`，移机时需提供本机可用的浏览器或调整执行器路径。

## 手机截图

以下为真实浏览器截图，不是设计稿。主表为 WebKit；Chromium 对应截图位于 `garden-layout/chromium/390/` 和 `430/`。

| 页面 | 粉色390px | 粉色430px | 绿色390px | 绿色430px |
|---|---|---|---|---|
| 首页 | [查看](garden-layout/webkit/390/pink-home.jpg) | [查看](garden-layout/webkit/430/pink-home.jpg) | [查看](garden-layout/webkit/390/green-home.jpg) | [查看](garden-layout/webkit/430/green-home.jpg) |
| 选题 | [查看](garden-layout/webkit/390/pink-setup.jpg) | [查看](garden-layout/webkit/430/pink-setup.jpg) | [查看](garden-layout/webkit/390/green-setup.jpg) | [查看](garden-layout/webkit/430/green-setup.jpg) |
| 答题 | [查看](garden-layout/webkit/390/pink-drill.jpg) | [查看](garden-layout/webkit/430/pink-drill.jpg) | [查看](garden-layout/webkit/390/green-drill.jpg) | [查看](garden-layout/webkit/430/green-drill.jpg) |
| 结果 | [查看](garden-layout/webkit/390/pink-result.jpg) | [查看](garden-layout/webkit/430/pink-result.jpg) | [查看](garden-layout/webkit/390/green-result.jpg) | [查看](garden-layout/webkit/430/green-result.jpg) |
| 套卷目录 | [查看](garden-layout/webkit/390/pink-paper.jpg) | [查看](garden-layout/webkit/430/pink-paper.jpg) | [查看](garden-layout/webkit/390/green-paper.jpg) | [查看](garden-layout/webkit/430/green-paper.jpg) |
| 单题 | [查看](garden-layout/webkit/390/pink-detail.jpg) | [查看](garden-layout/webkit/430/pink-detail.jpg) | [查看](garden-layout/webkit/390/green-detail.jpg) | [查看](garden-layout/webkit/430/green-detail.jpg) |
| 生词 | [查看](garden-layout/webkit/390/pink-words.jpg) | [查看](garden-layout/webkit/430/pink-words.jpg) | [查看](garden-layout/webkit/390/green-words.jpg) | [查看](garden-layout/webkit/430/green-words.jpg) |
| 外观 | [查看](garden-layout/webkit/390/pink-appearance.jpg) | [查看](garden-layout/webkit/430/pink-appearance.jpg) | [查看](garden-layout/webkit/390/green-appearance.jpg) | [查看](garden-layout/webkit/430/green-appearance.jpg) |

修改前首页：[390px](garden-layout/webkit/390/before-home.jpg) / [430px](garden-layout/webkit/430/before-home.jpg)。

## Claude 更新原 Artifact 时

1. 从 `claude/tender-hopper-moneok` 拉取本轮提交，运行 `python build/assemble.py`，确认 `site/index.html` 与仓库一致；不要从空白 main 发布。
2. 用生成的完整 `site/index.html` 更新 **原** Artifact `https://claude.ai/artifact/X2BfxTZwqhRZzaTo2Y4qEf`。保留原项目和原云端数据库关联。不要另建 Artifact 或网址，不要改成 localStorage 存学习进度。
3. 页面包含版本标识 `<meta name="garden-ui-version" content="2026-11-12-garden-layout">`。发布后核对实际页面版本与构建哈希，不能只凭 GitHub 分支或“发布成功”判断。
4. 在原账户的真手机上核对已有做题数量、备用、过、生词、备注和上次会话；然后切换粉色/森林/简洁，点击开始验证图片改变、答题中稳定。
5. 本环境访问原网址得到登录页，无法核实其登录后的真实页面或云端数据，也没有执行发布。上述手机实机与线上核对仍由原 Artifact 持有者完成。

回退时使用 `cd1a971` 对应完整 HTML，保持原 Artifact 的数据库绑定。如果此前选了新增森林皮肤，回退前先切到粉色或简洁；旧版没有森林皮肤样式。源码回退不应删除 progress/words/session 数据。
