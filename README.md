About the custodian project
===========================

This is the source code of automatic repository management system.

Explanations
------------

* data_collector.py

  basic parser for local repo. Will return a debian.deb822-like object.

* repo/ directory

  A dockerfile used to build repo/ docker image.

  Some action wrappers: docker-build, docker-run, docker-purge are included too.

  This docker image is still under development. If you start it with /bin/bash, you may interactively push packages into local debiancn repo.

custodian: 自定义deb软件源上传、构建和发布系统
===================================

总体设计目标是为了满足 repo.debiancn.org 系统的配置，最终形成一个 deb 软件包方便部署。

目标平台
--------

Debian 9 (Python3.5)

软件依赖
--------

* aptly - 处理并发布自定义软件源
* sbuild - 本地构建软件包
* mk-sbuild - 来自ubuntu-dev-tools，方便地创建sbuild环境
* python3 - 脚本语言解释器

工作流程
--------

1. 作为守护进程运行在后台
1. 经过触发或定期运行，检查 github: debiancn/repo 仓库的更新状态
1. 如果 git 仓库经过了更新，则进行如下操作：
    1. 如果源代码完全可用，获取并在本地完整构建并准备上传
    1. 如果属于仅提供二进制的包，检查上传队列是否存在文件并准备上传
    1. 同时定期检查上传队列并触发上传
1. 进行上传，发布通知消息（邮件？）并更新软件源，触发 json 文件更新机制

操作出错则邮件（？）提供错误信息。

目录结构
--------

```bash
CUSTODIAN_BASE_DIR="/srv/repo/"
CUSTODIAN_UPLOAD_DIR="${CUSTODIAN_BASE_DIR}/upload/"
CUSTODIAN_APTLY_BASE_DIR="${CUSTODIAN_BASE_DIR}/aptly/"
#CUSTODIAN_APTLY_SOCKET="${CUSTODIAN_APTLY_BASE_DIR}/aptly.sock" # needs newer aptly
CUSTODIAN_APTLY_SOCKET="127.0.0.1:8087"
CUSTODIAN_PUBLISH_DIR="${CUSTODIAN_APTLY_BASE_DIR}/public/" # determined by aptly
CUSTODIAN_SBUILD_BASE_DIR="${CUSTODIAN_BASE_DIR}/build/"
CUSTODIAN_SBUILD_BUILD_DIR="${CUSTODIAN_SBUILD_BASE_DIR}/sbuild/"
CUSTODIAN_SBUILD_LOG_DIR="${CUSTODIAN_SBUILD_BASE_DIR}/logs/"
```

备注
----

* aptly 带起来子进程（可丢弃 stdin/stdout/stderr），使用固定位置 UNIX socket 进行通信。
* 二进制上传（无 changes 文件）由文件夹名区分目标代号，其它信息由 aptly 完成。

