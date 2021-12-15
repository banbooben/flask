###
# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-05-10 21:24:13
 # @LastEditTime: 2021-10-21 14:00:34
 # @FilePath: /smfg_api/docker/build_image.sh
###

docker_app="flaskr"
image_name="sarmn/flaskr"
time=$(date "+%Y%m%d%H%M")

# 拷贝文件
copy_files(){

    # 创建文件夹
    mkdir ./${docker_app}

    # 拷贝相关资源
    cp -R ../application ./${docker_app}
    cp -R ../deploy ./${docker_app}
    cp ../Pipfile* ./${docker_app}

    # 删除多余无需打包文件
    cd ./${docker_app} && rm -f ./flask_app/logs/* && \
    rm -rf ./flask_app/migrations && rm -rf ./flask_app/static/upload/* && cd ..
}

# 开始构建镜像
start_build_image(){
    printf "\n================ Start build sarmn/flaskr:release_${time} image ================\n\n"
    echo "start build"
    docker build -f Dockerfile -t "${image_name}:release_${time}" .

    rm -rf ./${docker_app}

    docker images | grep "release_${time}"
}

# 推送镜像
push_image(){
    docker push "${image_name}:release_${time}"
}


start(){
  copy_files
  start_build_image
#  push_image
}

start
