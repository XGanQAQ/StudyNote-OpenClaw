## GitHub Actions 与 CI/CD 平台总结

### GitHub Actions 收费政策概览

GitHub Actions 的收费政策主要取决于仓库类型和运行器类型：

- **公共仓库：**
    - 使用 GitHub 托管的标准运行器**完全免费**。
    - 使用**自托管运行器**也**不收费**。
- **私有仓库：**
    - 提供一定的**免费分钟数和存储空间额度**（具体额度取决于 GitHub 订阅计划，例如 GitHub Free 每月 2,000 分钟和 500 MB 存储）。
    - 超出免费额度后，按使用量收费，费率因运行器类型（Linux、Windows、macOS、大型运行器等）和存储量而异。
    - 使用**自托管运行器免费**，因为你提供了计算资源，但需承担服务器及维护成本。
    - 可以设置**支出限制**以控制费用。

### GitHub Actions 的实现与性质

GitHub Actions **不是一个可下载的独立软件产品**，而是一个**深度集成在 GitHub 平台内的 CI/CD 服务或平台功能**。

- **实现方式：**
    - 通过 `.github/workflows/` 目录下的 **YAML 文件**定义**工作流 (Workflows)**。
    - 工作流由特定的 GitHub **事件 (Events)** 触发，包含一个或多个**作业 (Jobs)**。
    - 作业在**运行器 (Runners)** 上执行，运行器可以是 GitHub 托管的，也可以是自托管的。
    - 每个作业由一系列**步骤 (Steps)** 组成，可以是运行脚本或执行**操作 (Actions)**。
    - **操作 (Actions)** 是可重用的自动化单元，可以是 GitHub 官方提供、社区创建或自定义的。
- **开源性质：**
    - **GitHub Actions 运行器 (Runner) 是开源的**，其代码在 GitHub 上可查。
    - **GitHub 官方和社区创建的绝大多数 "Actions" 也是开源的**。
    - **GitHub Actions 平台本身（调度、UI、后端服务等）是闭源的**，作为 GitHub 的专有服务提供。

### 其他主流 CI/CD 平台/服务

除了 GitHub Actions，还有许多其他优秀的 CI/CD 平台和服务可供选择：

1. **Jenkins：** 最流行、最成熟的**开源** CI/CD 工具，插件生态极其丰富，高度可定制，但维护成本相对较高。
2. **GitLab CI/CD：** 作为 **GitLab 一体化 DevOps 平台**的一部分，与 GitLab 仓库无缝集成，配置即代码，功能全面。
3. **CircleCI：** 云端 CI/CD 服务，注重速度和效率，与 GitHub 和 Bitbucket 集成良好，尤其适合云原生和移动应用开发。
4. **Azure DevOps (Azure Pipelines)：** 微软提供的一站式 DevOps 平台，与 Azure 生态深度集成，功能强大，适合微软技术栈项目。
5. **AWS CodePipeline / CodeBuild / CodeDeploy：** 亚马逊 AWS 提供的一系列 CI/CD 服务，可组合使用，与 AWS 云服务深度集成。
6. **Bitbucket Pipelines：** Atlassian 提供，直接集成在 Bitbucket 仓库中，适合 Bitbucket 用户。
7. **Travis CI：** 老牌云端 CI 服务，与 GitHub 集成良好，对开源项目支持度高。
8. **TeamCity：** JetBrains 出品的 CI/CD 服务器，功能强大，界面友好，有免费和商业版，适用于企业级项目。

### 中国国内的 CI/CD 平台/服务

中国国内也有多款成熟的 CI/CD 平台，它们通常针对国内环境和用户需求进行优化：

1. **阿里云效 (Aliyun Yunxiao)：** 阿里云的一站式 BizDevOps 平台，与阿里云生态系统深度融合。
2. **腾讯云 CODING DevOps：** 腾讯云旗下的一站式软件研发管理平台，提供全面 DevOps 工具链，对小型项目友好。
3. **华为云 DevCloud (CodeArts)：** 华为云提供的 DevSecOps 平台，强调安全，与华为云生态紧密结合。
4. **极狐 GitLab：** GitLab 在中国的本地化发行版，提供 GitLab 所有功能及本地支持。
5. **Jenkins：** 尽管是国际开源工具，但在中国国内有大量企业自部署使用，以满足高度定制和数据安全需求。