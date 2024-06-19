DC = docker-compose
CONSUMER_APP = docker_compose/consumer.yaml
ENV = --env-file .env

.PHONY: consumer
consumer:
	$(DC) -f $(CONSUMER_APP) ${ENV} up --build -d

.PHONY: consumer-logs
consumer-logs:
	$(DC) -f $(CONSUMER_APP) ${ENV} logs -f

.PHONY: consumer-down
consumer-down:
	${DC} -f ${CONSUMER_APP} down
