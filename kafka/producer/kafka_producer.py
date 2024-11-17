from confluent_kafka import Producer
import time
def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

def produce_message():
    conf = {
        'bootstrap.servers': 'kafka:9092',  
        'client.id': 'airflow-producer',
        'acks':'all'
    }
    producer = Producer(conf)
    producer.produce('iot_data', key='device1', value='{"temperature": 25.5}',callback=acked)
    producer.flush()
    print("Message sent to Kafka")
    
produce_message()
