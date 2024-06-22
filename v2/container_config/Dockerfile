FROM debain

USER root

RUN apt-get update 

RUN apt-get install -y libmunge-dev libmunge2 munge \
libmariadb-dev libpam0g-dev libcgroup-dev libhwloc-dev \
build-essential fakeroot devscripts equivs \
hwloc libhwloc-dev git debhelper libncurses-dev libpam0g-dev \
libperl-dev liblua5.3-dev libhwloc-dev dh-exec librrd-dev \
libipmimonitoring-dev hdf5-helpers libfreeipmi-dev libhdf5-dev man2html \
libcurl4-openssl-dev libpmix-dev libhttp-parser-dev libyaml-dev libjson-c-dev \
libjwt-dev liblz4-dev libdbus-1-dev librdkafka-dev libreadline-dev perl libpam0g-dev \
wget curl openssh-server psmisc systemctl bpftrace libdbus-1-dev

RUN wget https://download.schedmd.com/slurm/slurm-23.11.1.tar.bz2

RUN tar -xaf slurm-23.11.1.tar.bz2

WORKDIR /slurm-23.11.1

RUN ./configure --prefix=/usr && make -j && make -j install 

RUN mkdir /run/munge

RUN chown -R munge: /etc/munge/ /var/log/munge/ /var/lib/munge/ /run/munge/ 

RUN mkdir /var/spool/slurmctld

RUN mkdir /var/spool/slurmd

RUN mkdir /var/spool/slurmdbd

RUN chown -R munge: /var/spool/slurmctld /var/spool/slurmd /var/spool/slurmdbd

RUN cp ./etc/slurmctld.service /lib/systemd/system/

RUN cp ./etc/slurmd.service /lib/systemd/system/

RUN cp ./etc/slurmdbd.service /lib/systemd/system/
