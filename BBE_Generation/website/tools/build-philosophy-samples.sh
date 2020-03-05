#!/usr/bin/env bash

BALLERINA_HOME=$2

CURRENT_DIR=$(pwd)
echo "....Building philosophy samples..."

if [ -z "$BALLERINACMD" ] ; then
  if [ -n "$BALLERINA_HOME"  ] ; then
	if [ $OSTYPE == "msys" ];
	  EXEC=""
	  then
		EXEC="bin/ballerina.bat"
	  else
        EXEC="bin/ballerina"
	fi
	BALLERINACMD=$BALLERINA_HOME$EXEC 
  else
    BALLERINACMD=ballerina
  fi
fi

if [ -z "$BALLERINA_HOME" ]; then
  echo "[ERROR] You must set the BALLERINA_HOME variable before building philosophy samples."
  exit 1
fi

if [ ! -x "$BALLERINACMD" && $OSTYPE -ne "msys" ] ; then
  echo "[ERROR] BALLERINA_HOME is not defined correctly."
  echo "[ERROR] cannot execute $BALLERINACMD"
  exit 1
fi

echo "Ballerina Home : $BALLERINA_HOME"
$BALLERINACMD -v

exit_on_error() {
    exit_code=$1
    file_name=$2

    if [ $exit_code -ne 0 ]; then
        >&2 echo "[ERROR] \"${file_name}\" failed with exit code ${exit_code}."
    fi
}

BUILDDIR=$1
if [ -z "$BUILDDIR" ]
  then
    echo "[ERROR] Source dir is not supplied"
    exit 1
fi

cd $BUILDDIR
for f in *.bal; do
  echo  "   Building $f"
  $BALLERINACMD build $f
  exit_on_error $? $f
done
cd $CURRENT_DIR