import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

params = pika.URLParameters('amqps://fmoufdkk:g-MYk67Qym_m4Mzpesrx-52-sZssSwn1@jackal.rmq.cloudamqp.com/fmoufdkk')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
  print('Receive in admin')
  id = json.loads(body)
  product = Product.objects.get(id=id)
  product.likes = product.likes+1
  product.save()
  print('Product likes incresed.')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close