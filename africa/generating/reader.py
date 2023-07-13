import pika
import json
import csv
import datetime
import psycopg2

con = psycopg2.connect(
    database="africa",
    user="postgres",
    password="qwer1234",
    host="127.0.0.1",
    port="5432"
)
cur = con.cursor()

with open('rabbit_config.json') as f:
    config = json.load(f)

rabbitmq_config = config['rabbitmq']
RABBITMQ_HOST = rabbitmq_config['host']
RABBITMQ_PORT = rabbitmq_config['port']
RABBITMQ_USER = rabbitmq_config['user']
RABBITMQ_PASSWORD = rabbitmq_config['password']
QUEUE_NAME = rabbitmq_config['queue_name']

# Функция, которая обрабатывает сообщение из очереди RabbitMQ
with open('temperature.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)


    def process_message(ch, method, properties, body):
        parsed_data = json.loads(body)

        temperature = parsed_data['temperature']
        date = parsed_data['date']
        sensor_id = parsed_data['id']
        writer.writerow([sensor_id, date, round(temperature, 1)])
        cur.execute(
            "INSERT INTO raw_data (SENSOR_ID,DATE,TEMPERATURE) VALUES (parsed_data['id'], parsed_data['date'], parsed_data['temperature'])"
        )


    # Подключение к очереди RabbitMQ и получение сообщений
    def connecting(connection):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST, port=RABBITMQ_PORT,
            virtual_host='/', credentials=pika.PlainCredentials(
                RABBITMQ_USER, RABBITMQ_PASSWORD)))

        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message, auto_ack=True)
        channel.start_consuming()
