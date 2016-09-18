#!/usr/bin/env bash

TESTS_FOLDER="app/test/"
TEST_FILE_PATTERN="*-tests.py"

coverage erase

for file in $(find $TESTS_FOLDER -name "$TEST_FILE_PATTERN")
do
  # replace all slashes in the filename with periods
  testfile=${file//\//\.}
  # remove the remaining `.py` at the end of the filename
  testmodule=${testfile::-3}
  # run the test
  coverage run -am $testmodule
done
