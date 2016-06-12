#!/bin/bash

pushd 'nbbuild/netbeans'
sed -i 's; -splash:\\"\${cachedir}/splash.png\\";;' 'platform/lib/nbexec'
popd
