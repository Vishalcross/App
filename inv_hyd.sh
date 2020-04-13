curl --silent http://10.19.1.2:8888/compute/v1/apps/$1/instances | jq . | jq .[] | jq '.hostname +" "+ .primary_ip + " " + .instance_type'| grep $2
