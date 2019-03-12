#!/bin/bash

# Data Insert
sqlite3 awscli.sqlite3 'drop table timeline;'
echo "InstanceType,InstanceId,InstanceCost" > cost-schema.csv
aws ec2 describe-instances \
	| jq -r -c '.Reservations[].Instances[] | select(.State.Name == "running") | [.InstanceType, .InstanceId] | @csv' \
	| awk -F',' '{print $1","$2","}' \
        > cost-data.csv
cat cost-schema.csv > output.csv
cat cost-data.csv >> output.csv
sqlite3 -separator ',' awscli.sqlite3 '.import output.csv timeline'
sqlite3 awscli.sqlite3 "select InstanceType, InstanceId from timeline;"

