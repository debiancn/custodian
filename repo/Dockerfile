FROM debian:testing
LABEL Description="working environment for aptly" Version="1.0"

# Set TERM environment variable first
ENV TERM xterm

# First, use sed to select a local mirror
RUN sed -i 's/deb.debian.org/ftp.cn.debian.org/g' /etc/apt/sources.list \
  && sed -i 's/security.debian.org/ftp.cn.debian.org\/debian-security/g' /etc/apt/sources.list
RUN apt-get update
#RUN apt-get -y dist-upgrade

# aptly is mandatory for this docker
RUN apt-get -y install vim aptly zsh wget locales python3 python3-debian \
  python3-apt python3-pyinotify htop graphviz git curl devscripts tmux \
  && apt clean

# - Set the locale + timezone --------------------------------------------------
RUN echo "Asia/Shanghai" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    sed -i -e 's/# zh_CN.UTF-8 UTF-8/zh_CN.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    echo 'LANG="zh_CN.UTF-8"'>/etc/default/locale && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=zh_CN.UTF-8

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

# mount data directory
#VOLUME /data
# instead, please use -v /data:/data during docker run

# Statically put gpg data into /root, for repo signing
ADD .gnupg /root/.gnupg
# Add aptly config file
ADD aptly.conf /etc/aptly.conf
# Add my program
ADD scripts /root/scripts

# Fix permission for /root/.gnupg
RUN chmod 700 /root/.gnupg

# Install oh-my-zsh
# XXX: still with error code. Needs debugging.
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" \
  || true
RUN sed -i -e 's/ZSH_THEME="robbyrussell"/ZSH_THEME="ys"/' /root/.zshrc \
  && chsh root --shell /usr/bin/zsh

# Setup git identity
RUN git config --global user.email "repo@debiancn.org" \
  && git config --global user.name "DebianCN Repo Admin"

CMD /bin/sh -c "(/root/scripts/update-repo-metadata > /dev/null 2> /dev/null < /dev/null &); export TERM=xterm; /usr/bin/zsh"
