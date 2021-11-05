get_latest_release() {
  curl --silent "https://api.github.com/repos/$1/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/'
}

TUPROLOG_GITHUB='tuProlog/2p-kt'
TUPROLOG_VERSION=`get_latest_release $TUPROLOG_GITHUB`
TUPROLOG_JAR_URL="https://github.com/$TUPROLOG_GITHUB/releases/download/$TUPROLOG_VERSION/2p-$TUPROLOG_VERSION-full.jar"

rm -rf tuprolog/libs/*.jar

wget -P tuprolog/libs/ $TUPROLOG_JAR_URL || (echo "Failed to download $TUPROLOG_JAR_URL"; echo "Ensure command wget is installed (brew install wget on Mac OS)")
