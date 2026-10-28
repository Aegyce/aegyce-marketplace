# Aegyce Marketplace

Aegyce Marketplace 按 Agent 分类，分发各 Agent 中可复用的组件。组件可包括 Skill、MCP 集成、工具，以及 AI 工具支持的其他能力。<br>
Aegyce Marketplace distributes reusable components from Aegyce agents, with plugins grouped by agent. Components may include skills, MCP integrations, tools, and other capabilities supported by AI tools.

## 当前插件<br>Available plugins

### Aesy

- [Aesy:computer-technical-language](https://github.com/Aegyce/agent-aesy/tree/main/plugins/computer-technical-language)：提供计算机技术用语 Skill，用于编写、润色和审查技术文档、代码注释与技术答复。<br>
  Provides guidance on terminology and wording when drafting, revising, or reviewing technical documentation, code comments, and technical responses.

## 使用方式<br>Usage

1. 在 AI 工具的插件市场管理页面选择“添加市场”，来源填写 `https://github.com/Aegyce/aegyce-marketplace.git`。<br>
   Open the plugin marketplace settings in your AI tool, choose Add marketplace, and enter `https://github.com/Aegyce/aegyce-marketplace.git` as the source.
2. 如需填写 Git 引用，使用 `main`；稀疏路径留空。<br>
   If a Git reference is required, use `main` and leave the sparse path empty.
3. 打开 Aegyce Marketplace，选择所需能力包并安装；例如 `Aesy:computer-technical-language`。<br>
   Open Aegyce Marketplace and install the capability package you need, such as `Aesy:computer-technical-language`.
4. 市场内容更新后，在所用的 AI 工具中刷新市场，再检查已安装插件是否有更新。<br>
   When the catalog changes, refresh the marketplace in your AI tool, then check installed plugins for updates.

上述步骤适用于支持此市场格式的 AI 工具，具体入口名称以相应工具的界面为准。安装插件时会安装其中的全部组件；不同能力包可以分别选择和安装。<br>
These steps apply to AI tools that support this marketplace format; refer to your tool’s interface for the exact labels. Installing a plugin installs all of its components. You can choose and install each capability package separately.

## 许可<br>License

原创内容采用 [CC BY-NC 4.0](LICENSE) 许可，商业用途须取得[单独书面授权](COMMERCIAL-LICENSE.md)。<br>
Original materials are licensed under [CC BY-NC 4.0](LICENSE). Commercial use requires [separate written permission](COMMERCIAL-LICENSE.md).
