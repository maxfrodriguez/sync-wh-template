#!/bin/sh
#
echo "iAnywhere Solutions, Inc. One Sybase Drive, Dublin, CA 94568, USA"
echo "Copyright (c) 2001-2012, iAnywhere Solutions, Inc. Portions copyright (c) "
echo "1988-2012, Sybase, Inc. All rights reserved. All unpublished rights reserved."
echo 

# the following lines set the SA location.
SQLANY12="/opt/sqlanywhere12"
export SQLANY12

[ -r "$HOME/.sqlanywhere12/sample_env32.sh" ] && . "$HOME/.sqlanywhere12/sample_env32.sh" 
[ -z "${SQLANYSAMP12:-}" ] && SQLANYSAMP12="/opt/sqlanywhere12/samples"
export SQLANYSAMP12

# the following lines add SA binaries to your path.
PATH="$SQLANY12/bin32:$SQLANY12/bin64:${PATH:-}"
export PATH
LD_LIBRARY_PATH="$SQLANY12/lib64:${LD_LIBRARY_PATH:-}"
LD_LIBRARY_PATH="$SQLANY12/lib32:${LD_LIBRARY_PATH:-}"
export LD_LIBRARY_PATH
