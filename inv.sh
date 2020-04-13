curl --silent http://10.47.255.6:8080/compute/v1/apps/$1/instances | jq . | jq .[] | jq '.hostname +" "+ .primary_ip + " " + .instance_type'
