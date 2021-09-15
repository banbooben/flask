###
# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-05-13 16:51:33
# @LastEditTime: 2021-04-11 11:41:24
# @FilePath: /flask/docker/build_base_image.sh
###

printf "\n================ Start build lnpy39:slim image ================\n\n"
cat >sources.list << EOF
deb http://mirrors.aliyun.com/debian/ buster main non-free contrib
deb http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib
deb http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib
deb http://mirrors.aliyun.com/debian-security/ buster/updates main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ buster main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib
deb-src http://mirrors.aliyun.com/debian-security/ buster/updates main non-free contrib
EOF
docker build -f Dockerfile.base -t sarmn/python:3.9.6-slim .
echo "ok"
docker push sarmn/python:3.9.6-slim
