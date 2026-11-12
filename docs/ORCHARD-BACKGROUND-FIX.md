# 橘园 N1 背景修复：已完成代码，交回原 Artifact 发布

基线：dcf3f44be4f41b73a225a908e47492a35da6dd95。修复提交回claude/tender-hopper-moneok，不改main、不新建网站、不自行发布。此前f7d341b原图与dcf3f44也保留备份。

## 修复了什么

1. 橘园顶部栏改为随页面滚动，不再以吸顶blur(10px)遮住经过的标题；背景透明，原返回/同步/设置控件保留。
2. 橘园的--glass改为none，去掉原blur(14px)毛玻璃；删除#bgimg::after整幅白粉渐变。原卡片底色、按钮、形状、间距和背景图片不重新设计。
3. “每页随机”为7类页面各分配一张不同的原图，首次打开时分配一次；返回、筛选、输入、云端快照或普通render不会重新抽图。做题时换题仍保持这类页面的背景，避免干扰。外观窗口的随机按钮改名“每页随机”。
4. 手动固定选图和简洁主题仍保留。**用户以前保存了固定图时仍会全站固定；要按页不同，需要在外观点“每页随机”。** 不强行覆盖现有外观偏好。

## 修改范围与数据保护

- build/template.html：三处原样式直接修改；皮肤块中的图片分配；render里调用applySkin；随机按钮文案。没有在末尾叠加一套全站覆盖样式。
- site/index.html：由原assemble.py重新生成，题库JSON与8张JPEG仍内嵌，无需新目录或新域名。
- README和本交接、测试、手机截图。

为了实现切换页面换背景，确有少量**表现层JavaScript**改动，已经具体列明；不是谎称整份JS逐字未变。除皮肤块、render的单次调用及随机按钮文案外，脚本与基线逐字一致。全部存储、判分、选项、标词、备注、data-act/data-k/data-q/data-n、题库和session逻辑均逐字保持。没有新增存储键、迁移/清空记录、重排题号，也没有访问真实账户数据库。

随机背景使用crypto的独立取样；不消费做题Math.random。测试核对初始Math.random调用为0。8张JPEG与基线逐字节一致，生成后的8条data URI解码后也完全一致。build/data.json及q2026.py完整保持。

## 验证

[源码边界检查](orchard-background-fix/source-check.json)核对原题库、构建脚本、图片、存储和交互代码的边界，生成页完全匹配模板及题库，JS可解析。

[Chromium记录](orchard-background-fix/chromium/verification.json) · [WebKit记录](orchard-background-fix/webkit/verification.json)

两种真实浏览器分别390px/430px检查：

- 顶部实际computed backdrop-filter为none、position为relative，滚动时顶部离开视口，不遮住下方标题；背景伪元素content为none，--glass为none。
- 7类页面7张不同背景；反复返回、5轮数据渲染均稳定。没有横向页面溢出。
- 外观8张原图都能解码显示，固定选图在7类页面及刷新后仍固定；简洁主题和切回橘园正常。
- 真实点击做题选项并交卷、写备注保存、标生词保存，再刷新读取；旧测试掌握/备用/生词记录保留。测试在兼容Artifact API的隔离内存数据库完成。
- 页面JS错误为0。没有连接、读取或写入本人真实Claude数据库。截图进度均为隔离测试值，不代表本人进度。

本地测试壳只提供Artifact宿主负责的viewport元信息；图片、CSS、HTML和实际交互来自生成页。外部字体请求在本地测试中隔离，未改变产品字体文件或声明。Linux WebKit移动端仿真，不是真实iPhone；不把本地通过冒充已上线或真实账号验收。

## 手机截图（真实浏览器，原尺寸）

以下为WebKit，两种宽度各自截图，未拼接或绘制替代页面。before/after首页均固定同一张背景2，方便只比较遮挡变化；random各页体现不同场景。

| 内容 | 390px | 430px |
| --- | --- | --- |
| 修改前首页 | [查看](orchard-background-fix/webkit/390/before-home.jpg) | [查看](orchard-background-fix/webkit/430/before-home.jpg) |
| 修改后首页 | [查看](orchard-background-fix/webkit/390/after-home.jpg) | [查看](orchard-background-fix/webkit/430/after-home.jpg) |
| 修改前滚动遮挡 | [查看](orchard-background-fix/webkit/390/before-scrolled.jpg) | [查看](orchard-background-fix/webkit/430/before-scrolled.jpg) |
| 修改后滚动清晰 | [查看](orchard-background-fix/webkit/390/after-scrolled.jpg) | [查看](orchard-background-fix/webkit/430/after-scrolled.jpg) |
| 套卷页面背景 | [查看](orchard-background-fix/webkit/390/paper-random.jpg) | [查看](orchard-background-fix/webkit/430/paper-random.jpg) |
| 做题页面背景 | [查看](orchard-background-fix/webkit/390/drill-random.jpg) | [查看](orchard-background-fix/webkit/430/drill-random.jpg) |
| 外观与8张缩略图 | [查看](orchard-background-fix/webkit/390/appearance-gallery.jpg) | [查看](orchard-background-fix/webkit/430/appearance-gallery.jpg) |
| 实际答题结果 | [查看](orchard-background-fix/webkit/390/answer-result.jpg) | [查看](orchard-background-fix/webkit/430/answer-result.jpg) |

## 给 Claude 的发布交接

请从claude/tender-hopper-moneok拉取包含本修复的最新提交，不要从main或恢复旧模板。先读差异、运行上述源码检查及python3 build/assemble.py；生成后工作区应无site/index.html差异。

本次已给出生成后的site/index.html，可在**同一个Artifact项目/原网址**更新，不另开Artifact或新域名；保留原数据库与记录。发布后用原账号核对旧掌握/备用/备注/生词，再在外观切换“每页随机”检查不同页面，及手动选图后的固定行为。用户原固定背景偏好不会被本轮强制覆盖。

本轮GPT未发布，所以当前线上页面在Claude更新前仍可能是旧效果；不要把提交GitHub说成已更新线上。代码回退可用dcf3f44，本轮未改变题库ID与存储结构，不涉及数据回退。
