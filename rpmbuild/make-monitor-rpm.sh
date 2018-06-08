#!/bin/bash
NAME='factory-monitor'
VERSION=${1:-0.1}
RELEASE=${2:-1}

ROOT_DIR="$(dirname $0)/.."

TMP_DIR=${NAME}-${VERSION}

mkdir -p $TMP_DIR/{aggregator,config,crontab,http,init.d,logrotate,messenger/outbox}
cp $ROOT_DIR/monitor.py $TMP_DIR/
cp $ROOT_DIR/aggregator/*.py $TMP_DIR/aggregator/
cp $ROOT_DIR/config/config.json $TMP_DIR/config/
cp $ROOT_DIR/config/*.py $TMP_DIR/config/
cp $ROOT_DIR/http/*.py $TMP_DIR/http/
cp $ROOT_DIR/messenger/*.py $TMP_DIR/messenger/
cp $ROOT_DIR/crontab/factory-monitor $TMP_DIR/crontab/
cp $ROOT_DIR/init.d/factory-monitor $TMP_DIR/init.d/
cp $ROOT_DIR/logrotate/factory-monitor $TMP_DIR/logrotate/
cp $ROOT_DIR/rpmbuild/factory-monitor.spec $TMP_DIR/

tar -czvf ${NAME}-${VERSION}.tgz ${NAME}-${VERSION}/

mkdir -p RPMBUILD/{RPMS/noarch,SPECS,BUILD,SOURCES,SRPMS}
rpmbuild --define "_topdir `pwd`/RPMBUILD" \
         --define "ver ${VERSION}"         \
         --define "rel ${RELEASE}"         \
         --define "name ${NAME}"           \
         -tb ./${NAME}-${VERSION}.tgz

find RPMBUILD/ -type f -name "*.rpm" -exec mv {} . \;
rm -rf RPMBUILD/ ${NAME}-${VERSION}/ ./${NAME}-${VERSION}.tgz
