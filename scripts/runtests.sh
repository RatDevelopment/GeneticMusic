#!/usr/bin/env bash

TESTS_FOLDER="app/test/"
TEST_FILE_PATTERN="*-tests.py"

for file in $(find $TESTS_FOLDER -name "$TEST_FILE_PATTERN")
do
  testfile=${file//\//\.}
  coverage run -m ${testfile::-3}
done
