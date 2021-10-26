#! /bin/bash

cd /home/edoardo/secondary-checkout
git submodule update --init --recursive
rm -rf target
if ! ./build -j8 target/intree/codeql ; then
	echo "Build failed, skipping commit";
	exit 125;
fi
export CODEQL_DIST="/home/edoardo/secondary-checkout/target/intree/codeql"
export PATH="/home/edoardo/secondary-checkout/target/intree/codeql:$PATH"
codeql test run --dil-tests semmlecode-nolang-tests/dil/basic/incremental.dil --search-path . --no-default-compilation-cache