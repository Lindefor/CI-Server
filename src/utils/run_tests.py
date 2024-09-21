
import json
import subprocess


def run_tests(repo_path):
    """
    This function is called from the Flask POST endpoint /build that receives an API call from GitHub webhooks
    with changes from a pull requests. It then runs the tests on the specific commit.

    :return: A tuple containing a message and a status code.
    :rtype: tuple
    """
    install_command = ["npm", "install"]
    command = ["npx", "playwright", "test", "tests/test.ts"]

    subprocess.run(install_command, 
                   cwd=repo_path+"/")
    
    process = subprocess.run(command, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.STDOUT, 
                             universal_newlines=True,
                             cwd=repo_path+"/")
                            
    
    output = process.stdout
    return_code = process.returncode

    return return_code, output
    
