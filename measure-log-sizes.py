import os

for size in [1,2,3,4,5]:
    for min in [True, False]:
        name = "log-" + str(size)
        if min:
            name += "-min"
        name += "-counts.json"
        invocation = "codeql database analyze --ram 16000 --threads 8 --output=/home/edoardo/scratch/result.sarif --format=sarif-latest"
        invocation += " --search-path /home/edoardo/semmle-code/language-packs/go:/home/edoardo/semmle-code/ql"
        invocation += " --additional-packs /home/edoardo/semmle-code/ql"
        invocation += " --log-to-stderr --tuple-counting"
        invocation += f" --evaluator-log /home/edoardo/scratch/{name}"
        invocation += f" --evaluator-log-level {size}"
        if min:
            invocation += " --evaluator-log-minify"
        invocation += " /home/edoardo/codeql-databases/salt"
        invocation += " python-security-and-quality.qls"
        os.system("rm -rf /home/edoardo/codeql-databases/salt/db-python/default/cache")
        os.system("rm -rf /home/edoardo/codeql-databases/salt/results")
        os.system(invocation)