from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import json
import time
import argparse
import socket

# Kafka 配置
BOOTSTRAP_SERVERS = 'localhost:9092'  # 默认本地地址
TOPIC_NAME = 'fastapi-kafka'  # 测试用主题
GROUP_ID = 'test_group'  # 消费者组ID


def test_kafka_connection():
    """测试是否能连接到 Kafka 服务器"""
    try:
        # 创建临时生产者测试连接
        test_producer = Producer({
            'bootstrap.servers': BOOTSTRAP_SERVERS,
            'client.id': socket.gethostname(),
            'message.timeout.ms': 3000  # 3秒超时
        })

        # 尝试刷新生产者（强制连接）
        test_producer.flush(timeout=3.0)
        print("✅ 成功连接到 Kafka 服务器")
        return True
    except KafkaException as e:
        print(f"❌ Kafka 连接错误: {e}")
        if e.args[0].code() == KafkaError._TIMED_OUT:
            print("   原因: 连接超时，请检查:")
            print(f"    1. Kafka 是否在 {BOOTSTRAP_SERVERS} 运行?")
            print("    2. 防火墙是否阻止了连接?")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")
        return False


def delivery_report(err, msg):
    """生产者消息传递回调函数"""
    if err is not None:
        print(f'❌ 消息发送失败: {err}')
    else:
        print(f"✅ 消息已发送: [分区 {msg.partition()}] {msg.value().decode('utf-8')}")


def produce_messages(num_messages=5):
    """生产者：发送测试消息"""
    print(f"\n📤 生产者启动，将发送 {num_messages} 条消息到主题 '{TOPIC_NAME}'...")

    # 创建生产者配置
    conf = {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'client.id': socket.gethostname(),
        'message.timeout.ms': 5000,
        'acks': 'all'  # 确保消息被完全提交
    }

    try:
        producer = Producer(conf)

        # 发送消息
        for i in range(num_messages):
            message = {
                "id": i,
                "text": f"Confluent 测试消息 #{i}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            json_message = json.dumps(message)

            # 异步发送消息（带回调）
            producer.produce(
                TOPIC_NAME,
                key=str(i),
                value=json_message,
                callback=delivery_report
            )

            # 轮询事件（触发回调）
            producer.poll(0)
            time.sleep(0.5)  # 避免发送过快

        # 等待所有消息发送完成
        producer.flush()
        print("✅ 所有消息已发送成功！")
        return True

    except KafkaException as e:
        print(f"❌ Kafka 生产者错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")
        return False


def consume_messages(timeout=10):
    """消费者：接收消息"""
    print(f"\n📥 消费者启动，监听主题 '{TOPIC_NAME}'，等待 {timeout} 秒...")

    # 创建消费者配置
    conf = {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest',  # 从最早的消息开始
        'enable.auto.commit': False,  # 手动提交偏移量
        'max.poll.interval.ms': 600000  # 延长轮询间隔
    }

    try:
        consumer = Consumer(conf)
        consumer.subscribe([TOPIC_NAME])

        start_time = time.time()
        message_count = 0

        # 轮询消息
        while time.time() - start_time < timeout:
            msg = consumer.poll(timeout=1.0)  # 1秒超时

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # 分区结束（正常情况）
                    continue
                else:
                    print(f"❌ 消费者错误: {msg.error()}")
                    break

            # 成功接收消息
            try:
                message = json.loads(msg.value().decode('utf-8'))
                print(f"  收到消息: [分区 {msg.partition()}] {message['text']}")
                message_count += 1

                # 手动提交偏移量（确保至少一次处理）
                consumer.commit(asynchronous=False)
            except Exception as e:
                print(f"❌ 消息解析错误: {str(e)}")

        print(f"✅ 共收到 {message_count} 条消息")
        return True

    except KafkaException as e:
        print(f"❌ Kafka 消费者错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")
        return False
    finally:
        try:
            consumer.close()
        except:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Confluent Kafka 测试工具')
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