#!/bin/bash

readonly FILE='editor.settings.storage/src/org/netbeans/modules/editor/settings/storage/fontscolors/CompositeFCS.java'

if [[ -s "$FILE" ]] ; then
  sed -i 's/private static final int DEFAULT_FONTSIZE = 13;/private static final int DEFAULT_FONTSIZE = 9;/' "$FILE"
else
  echo "Known default configuration file not found: '$FILE'" >&2
  exit 1
fi
