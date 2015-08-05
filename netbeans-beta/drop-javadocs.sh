#!/bin/bash

pushd 'nbbuild'

readonly PROPERTIES=(
javadoc.packages
config.javadoc.stable
config.javadoc.devel
config.javadoc.friend
config.javadoc.deprecated
config.javadoc.all
config.jnlp.stable
)

: >'user.build.properties'
for prop in ${PROPERTIES[*]}
do
  echo "${prop}=" >>'user.build.properties'
done

popd
