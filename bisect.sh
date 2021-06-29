#! /bin/bash

cd /home/edoardo/secondary-checkout
git submodule update --recursive
#rm -rf target
if ! ./build -j8 target/intree/codeql ; then
	echo "Build failed, skipping commit";
	exit 125;
fi
export CODEQL_DIST="/home/edoardo/secondary-checkout/target/intree/codeql"
export PATH="/home/edoardo/secondary-checkout/target/intree/codeql:$PATH"
codeql resolve queries --search-path /home/edoardo/secondary-checkout/ql --format=bylanguage -- /home/edoardo/test-query-repo/js