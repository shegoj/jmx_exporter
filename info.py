"""
Use docker compose file in this directory to spin up the test Kafka/Zookeeper cluster
when running these tests:
    docker-compose -f docker-compose-kafka.yaml up
"""
import logging, sys
import threading
from nose.tools import assert_greater_equal

from jmxquery import JMXConnection, JMXQuery, MetricType

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    stream=sys.stdout,
                    level=logging.DEBUG)

CONNECTION_URL = "service:jmx:rmi:///jndi/rmi://localhost:49112/jmxrmi"

def test_wildcard_query():

    jmxConnection = JMXConnection(CONNECTION_URL)
    jmxQuery = [JMXQuery("*:*")]
    metrics = jmxConnection.query(jmxQuery)
    printMetrics(metrics)

def printMetrics(metrics):
    for metric in metrics:
        if metric.metric_name:
            print(f"{metric.metric_name}<{metric.metric_labels}> == {metric.value}")
        else:
            print(f"{metric.to_query_string()} ({metric.value_type}) = {metric.value}")

    print("===================\nTotal Metrics: " + str(len(metrics)))


if __name__ == "__main__":
    test_wildcard_query()

