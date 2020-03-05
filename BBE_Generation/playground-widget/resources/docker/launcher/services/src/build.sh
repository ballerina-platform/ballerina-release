for balSource in *.bal
do
    ballerina build $balSource --experimental
done