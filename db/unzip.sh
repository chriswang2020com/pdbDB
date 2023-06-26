#!/bin/bash

# 检查output文件夹是否存在，不存在则创建
if [ ! -d "~/output" ]; then
  mkdir ~/output
fi


# 定义一个函数来处理单个目录
process_directory() {
    # 保存当前目录
    local current_dir=$1

    # 切换到当前目录
    cd "$current_dir"
    
   

    # 遍历当前目录下的所有文件和文件夹
    for file in $(ls -A); do          
        if [[ "$file" == *.tar ]]; then
            # 如果是tar文件，解压并删除
            echo "unzip"
            tar -xf "$file"
        elif [[ "$file" == *.tar.gz ]]; then
            # 如果是tar.gz文件，解压并删除
            echo "gz"
            tar -xzf "$file" 
        elif [[ "$file" == *.pdbqt ]]; then
            # 如果文件以pdbqt结尾，移动到../output
            mv "$file" ~/output
        fi
    done
   

    # 遍历当前目录下的所有文件和文件夹
    for file in $(ls -A); do
        if [ -d "$file" ]; then
            # 如果是文件夹，递归调用这个函数
            echo "dir"
            process_directory "$file"
            
        elif [[ "$file" == *.tar ]]; then
            # 如果是tar文件，解压并删除
            echo "unzip"
            tar -xf "$file"
        elif [[ "$file" == *.tar.gz ]]; then
            # 如果是tar.gz文件，解压并删除
            tar -xzf "$file"
        elif [[ "$file" == *.pdbqt ]]; then
            # 如果文件以pdbqt结尾，移动到../output
            mv "$file" ~/output
        fi
    done
    

    # 切换回上一个目录
    cd ..
}

# 从当前工作目录开始
process_directory .
