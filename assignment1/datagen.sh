#!/bin/bash
rm -f results.csv
echo "nodes,edges,solution method,solutions seen,adds,solution cost,time" >>results.csv
for nodes in {3..10}
do
minnodes=$((nodes-1))
maxnodes=$((nodes*(nodes-1)/2))
for edges in $(seq $minnodes $maxnodes)
do
if [ $edges -le 20 ] #before this rule was added the runtime escalated exponentially for exhaustive search and got way too long
then
python3 graph.py --nodes $nodes --edges $edges --seed 93391
echo "${nodes},${edges},exhaustive,$(python3 solver.py --exhaustive --no-graph)" >>results.csv
echo "${nodes},${edges},greedy,$(python3 solver.py --no-graph)" >>results.csv
fi
done
done
