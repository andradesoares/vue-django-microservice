import pika, json

params = pika.URLParameters('amqps://fmoufdkk:g-MYk67Qym_m4Mzpesrx-52-sZssSwn1@jackal.rmq.cloudamqp.com/fmoufdkk')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
  properties = pika.BasicProperties(method)
  channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
