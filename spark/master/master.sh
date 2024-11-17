#!/bin/bash

# Set default Spark Master host to hostname if not provided
export SPARK_MASTER_HOST=${SPARK_MASTER_HOST:-$(hostname)}
export SPARK_HOME=/opt/bitnami/spark  # Adjusted to match /opt/spark path from Dockerfile

# Load Spark configurations
source "$SPARK_HOME/sbin/spark-config.sh"
source "$SPARK_HOME/bin/load-spark-env.sh"

# Ensure log directory exists
mkdir -p $SPARK_MASTER_LOG

# Link stdout to Spark Master log for easier log access
ln -sf /dev/stdout $SPARK_MASTER_LOG/spark-master.out

# Start Spark Master
cd $SPARK_HOME/bin
$SPARK_HOME/sbin/../bin/spark-class org.apache.spark.deploy.master.Master \
    --host $SPARK_MASTER_HOST \
    --port ${SPARK_MASTER_PORT:-7077} \
    --webui-port ${SPARK_MASTER_WEBUI_PORT:-8080} >> $SPARK_MASTER_LOG/spark-master.out
