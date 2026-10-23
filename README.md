# Aegyce Marketplace

A unified marketplace for Aegyce agents, skills, and plugins, with reusable capabilities and links to independently maintained repositories.

Aegyce 的统一插件市场。小型能力包直接保存在本仓库；需要独立维护的 Agent 或插件可放在其他仓库，通过市场索引接入。当前提供可用于 Codex 与支持自定义插件市场的 ChatGPT 客户端的 skill 插件，Aegyce 原生 Agent 分发格式后续另行适配。

## 添加市场与安装

### Codex CLI

```bash
codex plugin marketplace add Aegyce/aegyce-marketplace
codex plugin add computer-technical-language@aegyce-marketplace
```

更新市场源：

```bash
codex plugin marketplace upgrade aegyce-marketplace
```

更新后在客户端检查已安装插件的版本；会话仍使用旧内容时，新建会话或重启客户端。市场源刷新与插件实际生效分别核对。

### ChatGPT

在支持该功能的客户端打开“添加插件市场”，填写：

| 字段 | 内容 |
| --- | --- |
| 来源 | `Aegyce/aegyce-marketplace` |
| Git 引用 | 留空使用默认分支，或填写 `main` |
| 稀疏路径 | 留空 |

添加后在 **Aegyce Marketplace** 中安装需要的插件。市场添加、插件安装与插件启用分别完成；仅添加市场不代表所有插件已经安装。

命令和目录约定见 [Codex CLI 文档](https://learn.chatgpt.com/docs/cli/reference)与[插件打包文档](https://developers.openai.com/plugins/build/plugins)。本仓库作为自定义市场分发，尚未提交到官方公共目录。

## 当前插件

| 插件 | 版本 | 用途 |
| --- | --- | --- |
| [计算机技术用语规范](plugins/computer-technical-language/README.md) | 0.1.0 | 规范术语、措辞、句式和主体表达，保留技术事实、条件与不确定性 |

## 仓库结构

```text
.agents/plugins/marketplace.json      市场名称与插件来源索引
plugins/
└── computer-technical-language/
    ├── plugin.json                  插件名称、版本、展示信息和许可标识
    ├── README.md                    插件用途和使用示例
    ├── LICENSE                      独立分发时保留的许可全文
    ├── COMMERCIAL-LICENSE.md         商业授权方式与版权声明
    └── skills/
        └── computer-technical-language/
            ├── SKILL.md             完整规则与执行方式
            └── agents/openai.yaml   Skill 展示信息
LICENSE                              本仓库默认许可全文
COMMERCIAL-LICENSE.md                许可范围与商业授权方式
AGENTS.md                            仓库维护约定
```

默认分支 `main` 保存市场索引和当前插件内容。每个插件一个目录，开发使用任务分支，版本写入各插件清单。需要发布固定版本时可使用带插件名的 Git 标签，例如 `computer-technical-language/v0.1.0`；该名称是示例，不表示标签已经创建。

### 接入独立仓库

`.agents/plugins/marketplace.json` 的 `plugins` 数组支持 Git 来源。插件位于独立仓库根目录时，来源写为：

```json
{
  "source": "url",
  "url": "https://github.com/OWNER/AGENT-REPO.git",
  "ref": "v1.0.0"
}
```

这是 `source` 字段的示例，地址和版本需要替换为真实值；插件名称、分类和安装策略仍按现有索引条目配置。位于远端子目录时使用 `git-subdir` 并指定 `path`。市场仅记录来源，外部插件的许可证由其所属仓库规定。

模型权重、大型数据集和媒体资源放在独立制品存储中，由对应插件记录来源、版本及校验信息，不作为市场目录的一部分提交。

## 维护与迁移

Skill 规则直接在对应插件的 `SKILL.md` 中维护。修改时同步检查插件版本、显示信息和使用说明，通过分支与 PR 评审。语言规则须结合上下文判断，不扩展为机械禁词表。

本仓库可以独立克隆，也可以作为更大项目中的独立 Git 仓库放置。文件引用以仓库或插件根目录为基准，不依赖父项目、本机绝对路径、外部符号链接或本机已安装的其他 skill。

- **移动本地工作副本**：整体移动仓库目录，保留隐藏目录 `.git` 和 `.agents`。未提交的修改也随目录保留。
- **更换机器**：先提交并推送需要保留的内容，再克隆仓库；未推送提交及未跟踪文件需另行备份。
- **已添加的市场源**：通过 GitHub 地址添加的源不受本地开发目录移动影响；通过本地路径添加的源，需要在客户端重新指向新位置。
- **更换 GitHub 地址**：同步更新 Git remote、README、插件清单中的仓库链接及用户的市场源配置。
- **单独迁出插件**：整体移动对应 `plugins/<name>/` 目录，保留清单、skill、许可证和商业授权说明，再修改市场索引。插件自身没有指向仓库外的本地依赖。

原项目中的用语规范是本插件的初始来源；插件运行不读取原项目文件，后续在本仓库独立维护。

## 许可

Copyright © 2026 Aegyce.

本仓库当前的原创 skill 指令、文档及配置材料使用 [CC BY-NC 4.0](LICENSE)：在遵守署名等许可条件的前提下，可用于非商业用途。商业用途须取得版权所有者的单独书面授权，申请方式见[商业授权说明](COMMERCIAL-LICENSE.md)。

后续加入的可执行代码须明确其适用许可；第三方材料和索引指向的外部插件保留各自许可。本仓库许可不自动授予使用这些材料的权利。
