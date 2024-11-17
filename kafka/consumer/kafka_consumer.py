from confluent_kafka import Consumer, KafkaException

def consume_message():
    print('abc')
    conf = {
        'bootstrap.servers': 'kafka:9092',  
        'group.id': 'docker-consumer-group',
        'auto.offset.reset': 'earliest'
    }
    
    consumer = Consumer(conf)
    print("Starting consumer...")
    consumer.subscribe(['iot_data'])
    print("Subscribed to topic iot_data")

    
        
print('abce')        
consume_message()    
print('dabc')
