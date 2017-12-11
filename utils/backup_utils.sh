#!/usr/bin/env bash
#>utils.txt #clear file
current_repo=$(git config --get remote.origin.url);
for dir in ./*/
do
	cd $dir;
	util_repo=$(git config --get remote.origin.url);
	[ "$util_repo" != "$current_repo" ] &&
		git config --get remote.origin.url >>../utils.txt 
	cd ..;
done
