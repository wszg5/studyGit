#!/usr/bin/env bash
mkdir target
rm -f ./target/ztask.abc
rm -f ./target/ztask_package.zip
7za a -t7z  -pUFE*GHU=IK#7suw6o54w3e9987we2 -mhe -r ./target/ztask.abc .   -xr@.zipignore

#7za a -t7z -pUFE*GHU=IK#7saudfwe2 -mhe -r ./target/ztask.abc .   -xr\!bbb
7za a -tzip ./target/ztask_package.zip ./target/ztask.abc ./ztask.info ./ztask.sh

rm -f ./target/ztask.abc

echo "SUCCESS for target/ztask_package.zip"