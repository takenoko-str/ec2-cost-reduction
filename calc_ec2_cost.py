import boto3
import sqlite3

client = boto3.client('ec2')
dbname = 'awscli.sqlite3'

if __name__ == "__main__":
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    d = conn.cursor()
    # インスタンスIDとインスタンスタイプの情報
    for row in c.execute('SELECT InstanceId, InstanceType FROM timeline;'):
        instance_id, instance_type = row
        # インスタンスコストの情報
        for ic in d.execute("SELECT InstanceCostPerHour from cost WHERE InstanceType == '{}';".format(instance_type)):
            cost = float(ic[0])
            JPY_USD=111
            start_time=0
            end_time=24
            COST_DAY=cost * JPY_USD * (end_time - start_time)
        # １日のコストを集計し記録
        d.execute("UPDATE timeline SET InstanceCost = '{}' WHERE InstanceId = '{}';".format(COST_DAY, instance_id))
        # マネージメントコンソール上に反映
        response = client.create_tags(
                Resources=[instance_id],
                Tags=[{
                    'Key': 'CostCenter',
                    'Value': '{:.0f}円/日'.format(COST_DAY)
                }])
    
        #print("{:.0f}".format(COST_DAY), instance_id, instance_type)
    conn.commit()
    conn.close()
    
