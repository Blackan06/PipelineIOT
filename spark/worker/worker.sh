#!/bin/bash

export SPARK_HOME=/opt/bitnami/spark  # Adjusted to match /opt/spark path from Dockerfile

# Load Spark configurations
source "$SPARK_HOME/sbin/spark-config.sh"
source "$SPARK_HOME/bin/load-spark-env.sh"

# Ensure log directory exists
mkdir -p $SPARK_WORKER_LOG

# Link stdout to Spark Worker log for easier log access
ln -sf /dev/stdout $SPARK_WORKER_LOG/spark-worker.out

# Start Spark Worker and connect to Spark Master
$SPARK_HOME/sbin/../bin/spark-class org.apache.spark.deploy.worker.Worker \
    --webui-port ${SPARK_WORKER_WEBUI_PORT:-8081} $SPARK_MASTER >> $SPARK_WORKER_LOG/spark-worker.out
