#!/bin/sh
export JAVA_HOME='/opt/tuxjdk/tuxjdk'
/opt/tuxjdk/tuxjdk/bin/$( basename "${BASH_SOURCE[0]}" ) "$@"
