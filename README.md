# Aegyce Marketplace

A unified marketplace for Aegyce agents and their reusable skills, with support for independently maintained repositories.

Aegyce 的统一插件市场，用于分发 Agent 能力包及其包含的 skills。小型能力包可以保存在本仓库；需要独立维护的 Agent 可以放在其他仓库，通过市场索引接入。

## 当前状态

当前仓库处于结构与命名规划阶段，仅发布本说明。市场索引和 Agent 能力包尚未发布，暂不提供可安装插件。

## Zenkie · 臻启

规划的首个 Agent 为 **Zenkie（臻启）**，类型为 Aegyce 的通用 Agent。

Requirement 负责需求的整体规划、分工、协调与验收。没有匹配的领域 Agent 时，由 Zenkie 承接 Requirement 委派的工作，通过 Workspace 组织 Task，调用所需模型、工具和 skills 完成执行，并向 Requirement 回报进展和结果。

Zenkie 的名称取意于创建者姓名拼音 `zengjianqi` 的首尾音节。名称用于标识通用 Agent，不改变其在 Aegyce 中的职责与管理关系。

### 首项 skill：计算机技术用语规范

`computer-technical-language` 作为 Zenkie 内的一项 skill 保存，约束计算机技术领域的术语、措辞、句式和主体表达，适用于技术文档、代码注释、运维说明、故障分析和技术交流。

该 skill 保留原有技术事实、约束、条件与不确定性；后续其他通用 skills 可加入 Zenkie 的同级 skill 目录。

## 规划结构

以下为拟采用的目录结构，不代表这些文件已经发布：

```text
aegyce-marketplace/
├── README.md
├── .agents/
│   └── plugins/
│       └── marketplace.json
└── plugins/
    └── zenkie/
        ├── plugin.json
        ├── README.md
        ├── LICENSE
        ├── COMMERCIAL-LICENSE.md
        └── skills/
            └── computer-technical-language/
                ├── SKILL.md
                └── agents/openai.yaml
```

市场条目对应 Zenkie 能力包，`computer-technical-language` 是包内 skill。Codex 与 ChatGPT 的插件清单用于相应客户端分发；Aegyce 原生 Agent 的身份、导入和运行机制按 Aegyce 架构另行适配。

默认分支 `main` 用于维护市场介绍、索引和已发布内容。初期按 Agent 目录组织能力包；需要独立维护时可迁到单独仓库，由市场索引引用。模型权重和大型数据集使用独立制品存储。

## 使用方式

市场索引和首个能力包发布后，计划通过支持自定义插件市场的 Codex CLI 或 ChatGPT 客户端添加本仓库，并选择安装 Zenkie。届时补充经过验证的安装与更新方法。

当前先通过 GitHub 维护与分发，官方公共目录上架后续另行考虑。

## 完整迁移

仓库作为 Aegyce 项目中的独立 Git 仓库维护，同时须支持独立克隆和整体迁移：

- 仓库及能力包内部使用相对路径，不依赖父项目文件、本机绝对路径或仓库外符号链接。
- 移动本地工作副本时保留整个目录，包括隐藏的 `.git`、`.agents` 及尚未提交的文件。
- 更换机器前，提交并推送需要保留的内容；未推送提交和未跟踪文件另行备份。
- 单独迁出 Agent 能力包时，保留其插件清单、skills、许可证及必要资源，并更新市场索引。
- GitHub 来源不受本地目录位置影响；本地路径来源在移动后需要更新客户端配置。

## 许可

Copyright © 2026 Aegyce.

本仓库原创文档和 skill 指令采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)：非商业用途须遵守署名等许可条件，商业用途须另行取得版权所有者的书面授权，法律允许无需许可的情形除外。

商业授权请联系 [Aegyce](https://github.com/Aegyce)，可通过本仓库 [Issues](https://github.com/Aegyce/aegyce-marketplace/issues) 发起咨询；咨询本身不构成授权。能力包发布时将附带完整许可文本与授权说明。第三方材料及外部 Agent 仓库沿用各自许可。
