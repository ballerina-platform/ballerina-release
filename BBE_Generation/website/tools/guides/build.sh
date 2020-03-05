#Generate guides
echo ".....Building guide pages....."
echo "node version is "; node -v;
mkdocs build;
for d in site/*/ ; do
    if [ -e "$d"README/index.html ]
    then
        # updating relative paths
        grep -rl '\.\.\/'  "$d"README/index.html   | xargs sed -i 's/\.\.\///g';
        mv "$d"README/index.html "$d";
    fi
done
cp index.html site/
if [ $OSTYPE == "msys" ];
    then
        cp -r site/ $1/
    else
        rsync -ir site/ $1/
fi
echo ".....Completed building guide pages....."