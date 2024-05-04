#!/bin/bash

# 循环生成从节点编号 $START_NODE 到 $END_NODE 的密钥对
START_NODE=17
END_NODE=92

for ((i=$START_NODE; i<=$END_NODE; i++)); do
    PRIVATE_KEY_FILE="chain node ${i}sk.pem"
    PUBLIC_KEY_FILE="chain node ${i}vk.pem"

    # 生成私钥
    openssl ecparam -name prime256v1 -genkey -noout -out "$PRIVATE_KEY_FILE"

    # 生成公钥
    openssl ec -in "$PRIVATE_KEY_FILE" -pubout -out "$PUBLIC_KEY_FILE"

    echo "Generated key pair for chain node $i"
done
