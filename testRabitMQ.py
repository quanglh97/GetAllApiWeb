import pika

connection = pika.BlockingConnection (pika.ConnectionParameters ( 'localhost' ))
channel = connection.channel ()
channel.queue_declare (queue = 'hello' )

channel.basic_publish (exchange = '' ,
                      routing_key = 'xin chào' ,
                      body = 'Xin chào Thế giới!' )
print ( "[x] Đã gửi 'Hello World!'" )


