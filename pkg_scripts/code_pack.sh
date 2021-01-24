#!/bin/bash
# remove the add repo part of postinst in VSCode

URL=$(curl -Ls -o /dev/null -w  %{url_effective} https://go.microsoft.com/fwlink/?LinkID=760868)

wget "$URL"

FILE=$(echo "$URL" | grep -o 'code_.*.deb')
MODIFIED=false

mkdir extract
mkdir build

dpkg-deb -R "$FILE" extract/

rm "$FILE"

# modify postinst
if [[ -e extract/DEBIAN/postinst ]]; then
  CHKSUM=$(md5sum extract/DEBIAN/postinst | cut -f 1 -d ' ')
  if [ "$CHKSUM" == "132f406af89d3c6fca8290a480280e80" ]; then
    sed -i '26,78d' extract/DEBIAN/postinst
    MODIFIED=true
  else
    echo -e "postinst file has been updated, please check it!\n"
  fi
else
  echo -e "file not exist!\n"
fi

if $MODIFIED; then
  dpkg-deb -b extract/ build/
  rm -rf extract/
  echo -e "cleaning... check build dir for new package\n"
else
  rm -rf extract/ build/
  echo -e "cleaning... no changes.\n"
fi
