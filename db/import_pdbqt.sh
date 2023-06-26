#!/bin/bash

# MySQL连接信息
mysql_host="localhost"
mysql_user="root"
mysql_password="000000"
mysql_db="molecule"
mysql_table="pdbqt_table"

cd ~/output || exit 1

# 文件目录和属性值范围
file_directory="~/output"
property_min=1
property_max=1000

# 生成随机数函数
random_float() {
    awk -v min=$1 -v max=$2 'BEGIN{srand(); printf "%.2f\n", min + rand() * (max - min)}'
}

# 导入数据到MySQL

for file_path in ~/output/*.pdbqt; do
    pdbqt_text=""
    while IFS= read -r pdbqt_line || [[ -n "$pdbqt_line" ]]; do
        if [[ $pdbqt_line == "REMARK"* ]]; then
            # 处理每个pdbqt文件的开始行
            pdbqt_text=$pdbqt_line
            property1=$(random_float $property_min $property_max)
            property2=$(random_float $property_min $property_max)
            property3=$(random_float $property_min $property_max)
        elif [[ $pdbqt_line == "ATOM"* || $pdbqt_line == "ENDBRANCH"* ]]; then
            # 处理每个pdbqt文件的ATOM行或者ENDBRANCH行
            pdbqt_text+=$'\n'$pdbqt_line
        fi
    done < "$file_path"
    # 使用base64进行编码以防止特殊字符干扰SQL查询
    pdbqt_text_base64=$(echo "$pdbqt_text" | base64 --wrap=0)
    
    # 将数据插入MySQL表中
    mysql -h $mysql_host -u $mysql_user -p$mysql_password -e "USE $mysql_db; INSERT INTO $mysql_table (pdbqt_text, property1, property2, property3) VALUES ('$pdbqt_text_base64', $property1, $property2, $property3);"
done
