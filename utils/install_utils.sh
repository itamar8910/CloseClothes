while IFS= read line;
do
git clone $line
done <utils.txt
