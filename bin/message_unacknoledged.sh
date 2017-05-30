#!/usr/bin/env bash

# Forgotten acknowledgment

# It's a common mistake to miss the basic_ack.
# It's an easy error, but the consequences are serious.
# Messages will be redelivered when your client quits (which may look like random redelivery),
# but RabbitMQ will eat more and more memory as it won't be able to release any unacked messages.

# In order to debug this kind of mistake you can use rabbitmqctl to print the messages_unacknowledged field:

docker-compose exec rabbitmq  rabbitmqctl list_queues name messages_ready messages_unacknowledged