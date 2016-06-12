#!/bin/bash

# cleaning up non-linux stuff:
pushd nbbuild/netbeans/ide/bin/nativeexecution
rm -rf Sun* Mac* Windows*
popd
pushd nbbuild/netbeans/profiler/lib/deployed
pushd jdk15
rm -rf hpux* mac solaris* windows*
popd
pushd jdk16
rm -rf hpux* mac solaris* windows*
popd
pushd cvm
rm -rf windows*
popd
popd
# cleaning up files we do not need:
find nbbuild/netbeans -name .lastModified -delete
find nbbuild/netbeans -name *.exe -delete
find nbbuild/netbeans -name *.dll -delete
find nbbuild/netbeans -name *.bat -delete
find nbbuild/netbeans -name *.cmd -delete
rm -f nbbuild/netbeans/nb.cluster.*.built nbbuild/netbeans/*.html nbbuild/netbeans/*.txt nbbuild/netbeans/*.properties nbbuild/netbeans/*.css
# we do not want javafx for now, untill someone will specifically ask for it:
rm -rf nbbuild/netbeans/javafx nbbuild/netbeans/harness/nbi/.common
# fixing end of lines from windows:
sed -i 's/\r$//' nbbuild/netbeans/java/maven/bin/m2.conf
