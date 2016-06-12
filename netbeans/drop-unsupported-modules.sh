#!/bin/bash

pushd 'nbbuild'

mv 'cluster.properties' 'cluster.properties.backup'

readonly CLUSTERS=(
nb.cluster.groovy
nb.cluster.javacard
nb.cluster.mobility
nb.cluster.php
nb.cluster.javafx
api.htmlui
templatesui
core.browser
core.browser.webview
core.browser.webview.jfxplatformbridge
libs.javafx
)

GREP=''
for cluster in ${CLUSTERS[*]}
do
  GREP="${GREP} -e ${cluster}"
done
cat 'cluster.properties.backup' | grep -v ${GREP} >'cluster.properties'

popd
