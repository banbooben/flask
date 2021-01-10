###
 # @Author: shangyameng
 # @Email: shangyameng@aliyun.com
 # @Date: 2020-05-13 16:51:33
 # @LastEditTime: 2020-07-15 09:09:39
 # @FilePath: /dockerProject/python3Nginx/build_base_image.sh
 ###

printf "\n================ Start build centos_lnpy37:latest image ================\n\n"
docker build -f Dockerfile -t lnpy38:slim_test .
