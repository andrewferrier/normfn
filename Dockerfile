FROM phusion/baseimage:0.9.15
ENV HOME /root
ENV LANG en_US.UTF-8
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
CMD ["/sbin/my_init"]
MAINTAINER Andrew Ferrier <andrew.ferrier@example.com>
RUN apt-get update && apt-get install -y git build-essential \
        checkinstall \
        gdebi-core \
        python \
        python3-dateutil \
        python3-flake8 \
        python3-pip \
        python3-reportlab \
        python3-pexpect \
        wget
WORKDIR /tmp
RUN pip3 install https://bitbucket.org/gutworth/six/get/tip.tar.gz
RUN pip3 install coloredlogs freezegun
RUN wget -O /etc/vim/vimrc.local https://raw.githubusercontent.com/tpope/vim-sensible/master/plugin/sensible.vim
COPY . /tmp/normalize-filename/
WORKDIR /tmp/normalize-filename
RUN make builddeb_real && sh -c 'ls -1 /tmp/normalize-filename/*.deb | xargs -L 1 gdebi -n' && cp /tmp/normalize-filename/*.deb /tmp
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /var/tmp/*
