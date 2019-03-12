#!/bin/bash

sqlite3 awscli.sqlite3 'drop table cost;'
sqlite3 -separator ',' awscli.sqlite3 '.import cost.csv cost'
sqlite3 awscli.sqlite3 "select InstanceCostPerHour from cost;"

