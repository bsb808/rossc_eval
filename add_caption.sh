#filename=`convert lena.jpg -ping -format "%t" info:`
fname=$1  # image file - the actual file
outfname=$2  # image file name to use for saving the file
ctext=$3 # caption text 
#tmpdir=$4


#filename=$(basename "$outfname")
#extension="${filename##*.}"
#fileiso="${filename%.*}"
#rarename="${tmpdir}/${fileiso}_rare.${extension}"
rarename=${outfname}

echo "Converting $fname to $rarename with caption <${ctext}>"

width=`identify -format %w $fname`; \
convert -background '#0008' -fill white -gravity center -size ${width}x30 \
          caption:"${ctext}" \
          $fname +swap -gravity south -composite  $rarename


#convert -background '#0008' -fill white -gravity center -size ${width}x30 \
#          caption:"${ctext}" \
#          $fname +swap -gravity south -composite  $rarename

