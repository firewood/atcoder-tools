#!/bin/bash

WORKSPACE_DIR=.
PROJECT_FILES_DIR=project_files
CONTEST_ID=$1

if [ -z "$CONTEST_ID" ]; then
  echo "Please specify the contest ID."
  exit
fi

atcoder-tools gen --config ./config.toml $*

if [ -d $CONTEST_ID ]; then
  for problem in `ls $PROJECT_FILES_DIR`; do
    source=$PROJECT_FILES_DIR/$problem
    destination=$WORKSPACE_DIR/$CONTEST_ID/$problem
    if [ -d $destination ]; then
      cp -a $source/* $destination/
      echo "Copied: $source"
    fi
  done
  open $CONTEST_ID
fi
