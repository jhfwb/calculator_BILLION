::#!/bin/bash 注释 暂时有问题CMD不能到git里面来
echo "-------Begin-------"
git add .
git commit -m $1
echo $1
git push origin master
echo "--------End--------"
pause
