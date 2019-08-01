import pika
import time

class MessageBase:
    def __init__(self, host, port, user, password, virtualhost, exchange, queue):
        self.exchage_name = exchange
        self.queue_name = queue

        url = 'amqp://{}:{}@{}:{}/{}'.format(
            user, password, host, port, virtualhost
        )
        params = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        # 交换机 ,不用缺省
        self.channel.exchange_declare(exchange=self.exchage_name, exchange_type='direct')
        # 队列
        self.channel.queue_declare(queue=self.queue_name, exclusive=False)

        # 绑定, 手动绑定指定交换机
        self.channel.queue_bind(queue=self.queue_name, exchange=self.exchage_name)

    def __enter__(self):
        return self.channel

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

class Producer(MessageBase):
    def produce(self, message):
        # message = '{}-data-{}'.format(self.queue_name, message)
        self.channel.basic_publish(
            exchange=self.exchage_name,
            routing_key=self.queue_name,
            body=message)


class Consumer(MessageBase):
    def consume(self):
        method, props, body = self.channel.basic_get(queue=self.queue_name, auto_ack=True)
        return body

# 应用? 测试代码

if __name__ == '__main__': #  被导入代码
    qs = ('urls', 'htmls', 'outputs')

    c1 = Producer('148.70.137.191', 5672, 'mwq', 'mwq', 'test', 'news', qs[0])
    c2 = Producer('148.70.137.191', 5672, 'mwq', 'mwq', 'test', 'news', qs[1])
    c3 = Producer('148.70.137.191', 5672, 'mwq', 'mwq', 'test', 'news', qs[2])
    for i in range(40):
        print(c1.produce('hello'))
        print(c2.produce('my'))
        print(c3.produce('hi'))