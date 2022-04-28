###
# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-05-13 16:51:33
# @LastEditTime: 2022-04-24 13:50:12
# @FilePath: /flask/docker/build_base_image.sh
###

printf "\n================ Start build sarmn/python:3.9-slim image ================\n\n"
docker build -f Dockerfile.base -t sarmn/python:3.9-slim .
echo "ok"
#docker push sarmn/python:3.9.6-slim
