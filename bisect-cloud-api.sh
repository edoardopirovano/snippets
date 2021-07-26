#! /bin/bash

export CODEQL_DIST="/home/edoardo/secondary-checkout/target/intree/codeql"
export PATH="/home/edoardo/secondary-checkout/target/intree/codeql:$PATH"
cd /home/edoardo/secondary-checkout
git submodule update --recursive
rm -rf target cloud-test/codeql-bundle.zip
if ! ./build -j8 target/intree/codeql ; then
	echo "Build failed, skipping commit";
	exit 125;
fi
if ! ./build target/zips/codeql-bundle.zip ; then
	echo "Build failed, skipping commit";
	exit 125;
fi
mv target/zips/codeql-bundle.zip cloud-test
./build -j4 target/test/cloud-qlapi-tests/results.xml