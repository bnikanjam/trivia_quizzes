#!/bin/bash

counter=1
while [ $counter -le 1000 ]
do
echo $counter
((counter++))
pytest -s -p no:warnings
sleep 10
#osascript -e 'display notification "Completed!"'
done
#echo All done
