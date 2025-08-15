#!/usr/bin/env python3
# coding: utf-8

"""
@File   : kafka-python-demo.py
@Author : lyf
@Date   : 2025/8/15
@Desc   : 
"""
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import time
import argparse

# Kafka 配置
BOOTSTRAP_SERVERS = 'localhost:9092'  # 默认本地地址
TOPIC_NAME = 'fastapi-kafka'  # 测试用主题


def test_kafka_connection():
    """测试是否能连接到 Kafka 服务器"""
    try:
        # 尝试创建临时消费者来检测连接
        consumer = KafkaConsumer(
            group_id='test_connection',
            bootstrap_servers=BOOTSTRAP_SERVERS,
            consumer_timeout_ms=3000  # 3秒超时
        )
        consumer.close()
        print("✅ 成功连接到 Kafka 服务器")
        return True
    except NoBrokersAvailable:
        print("❌ 无法连接到 Kafka 服务器，请检查：")
        print("1. Kafka 是否已启动？")
        print("2. 地址端口是否正确？(当前使用: {})".format(BOOTSTRAP_SERVERS))
        print("3. 防火墙是否阻止了连接？")
        return False
    except Exception as e:
        print(f"❌ 连接错误: {str(e)}")
        return False


def produce_messages(num_messages=5):
    """生产者：发送测试消息"""
    print(f"\n📤 生产者启动，将发送 {num_messages} 条消息到主题 '{TOPIC_NAME}'...")

    try:
        # 创建生产者（使用 JSON 格式）
        producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        # 发送消息
        for i in range(num_messages):
            message = {
                "id": i,
                "text": f"测试消息 #{i}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            producer.send(TOPIC_NAME, value=message)
            print(f"  已发送: {message['text']}")
            time.sleep(0.5)  # 避免发送过快

        producer.flush()  # 确保所有消息都已发送
        print(f"✅ 所有消息已发送成功！")
        return True

    except Exception as e:
        print(f"❌ 生产者错误: {str(e)}")
        return False


def consume_messages(timeout=10):
    """消费者：接收消息"""
    print(f"\n📥 消费者启动，监听主题 '{TOPIC_NAME}'，等待 {timeout} 秒...")

    try:
        # 创建消费者
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',  # 从最早的消息开始读取
            group_id='test_group',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        start_time = time.time()
        message_count = 0

        # 轮询消息
        while time.time() - start_time < timeout:
            records = consumer.poll(timeout_ms=1000)  # 每次轮询1秒

            if not records:
                continue

            for tp, messages in records.items():
                for message in messages:
                    print(f"  收到消息: [分区 {tp.partition}] {message.value['text']}")
                    message_count += 1

        print(f"✅ 共收到 {message_count} 条消息")
        return True

    except Exception as e:
        print(f"❌ 消费者错误: {str(e)}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kafka 连接测试工具')
    parser.add_argument('--test', action='store_true', help='仅测试连接')
    parser.add_argument('--produce', action='store_true', help='运行生产者')
    parser.add_argument('--consume', action='store_true', help='运行消费者')
    parser.add_argument('--full', action='store_true', help='完整测试（连接+生产+消费）')

    args = parser.parse_args()

    # 如果没有参数，显示帮助信息
    if not any(vars(args).values()):
        parser.print_help()
        exit(1)

    # 检查连接
    if not test_kafka_connection():
        exit(1)

    if args.test:
        exit(0)

    # 执行完整测试
    if args.full:
        if produce_messages():
            time.sleep(1)  # 给 Kafka 一些处理时间
            consume_messages()
        exit(0)

    # 单独执行生产者
    if args.produce:
        produce_messages()

    # 单独执行消费者
    if args.consume:
        consume_messages()