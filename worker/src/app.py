from services import Consumer

def print_msg(msg):
  print(msg)

if __name__ == '__main__':
  consumer = Consumer(uri='amqp://root:root@localhost:5030/', queue='iris.process', execute=print_msg)
  consumer.run()
