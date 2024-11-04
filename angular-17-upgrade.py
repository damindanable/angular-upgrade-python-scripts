import fileinput
import subprocess
import os
import shutil
import sys
from time import sleep
import sys
import random

folder_path = "."
jira_number = random.randint(10000,100000)
ticket_number = f"RMM-{jira_number}"
branch_name = f"feature/{ticket_number}/angular-17-upgrade"
package_json_file_name = f"{folder_path}/package.json"
package_lock_delete_path = f"{folder_path}/package-lock.json"
node_modules_delete_path = f"{folder_path}/node_modules"
angular_path = f"{folder_path}/angular.json"
polyfills_path = f"{folder_path}/src/polyfills.ts"
jenkins_file_path = f"{folder_path}/Jenkinsfile"
jenkins_search_words = {
 'quasar@release/v13': 'quasar@release/v14',
 'nodeVersion: 16': 'nodeVersion: 20'
}
apx_dialog_service_path = f"{folder_path}"
apx_dialog_service_words = {
 '@n-able/neb-common/apx-confirmation-dialog': '@n-able/neb-common/apx-dialog',
}

fields = {
    '"angular-in-memory-web-api"': '"angular-in-memory-web-api": "^0.17.0"',
    '"@angular/animations"': '"@angular/animations": "^17.3.11"',
    '"@angular/common"':'"@angular/common": "^17.3.11"',
    '"@angular/core"':'"@angular/core": "^17.3.11"',
    '"@angular/forms"':'"@angular/forms": "^17.3.11"',
    '"@angular/localize"':'"@angular/localize": "^17.3.11"',
    '"@angular/platform-browser"':'"@angular/platform-browser": "^17.3.11"',
    '"@angular/platform-browser-dynamic"':'"@angular/platform-browser-dynamic": "^17.3.11"',
    '"@angular/router"':'"@angular/router": "^17.3.11"',
    '"@angular-devkit/architect"':'"@angular-devkit/architect": "^0.1703.8"',
    '"@angular-devkit/build-angular"':'"@angular-devkit/build-angular": "^17.3.8"',
    '"@angular-devkit/core"':'"@angular-devkit/core": "^17.3.8"',
    '"@angular-eslint/builder"':'"@angular-eslint/builder": "^17.5.2"',
    '"@angular-eslint/eslint-plugin"':'"@angular-eslint/eslint-plugin": "^17.5.2"',
    '"@angular-eslint/eslint-plugin-template"':'"@angular-eslint/eslint-plugin-template": "^17.5.2"',
    '"@angular-eslint/schematics"':'"@angular-eslint/schematics": "^17.5.2"',
    '"@angular-eslint/template-parser"':'"@angular-eslint/template-parser": "^17.5.2"',
    '"@angular/cdk"':'"@angular/cdk": "^17.3.10"',
    '"@angular/cli"':'"@angular/cli": "^17.3.8"',
    '"@angular/compiler"':'"@angular/compiler": "^17.3.11"',
    '"@angular/compiler-cli"':'"@angular/compiler-cli": "^17.3.11"',
    '"@angular/language-service"':'"@angular/language-service": "^17.3.11"',
    '"@apollo/client"':'"@apollo/client": "^3.10.4"',
    '"ng-packagr"':'"ng-packagr": "^17.3.0"',
    '"angular-gridster2"':'"angular-gridster2": "^17.0.0"',
    '"angular-oauth2-oidc"':'"angular-oauth2-oidc": "^17.0.2"',
    '"apollo-angular"':'"apollo-angular": "^6.0.0"',
    '"devextreme"':'"devextreme": "23.2.4"',
    '"devextreme-angular"':'"devextreme-angular": "23.2.4"',
    '"rxjs"':'"rxjs": "^7.8.1"',
    '"graphql"': '"graphql": "^16.9.0"',
    '"eslint"':'"eslint": "^8.57.0"',
    '"odata-query"':'"odata-query": "^6.7.1"',
    '"typescript"':'"typescript": "~5.4.5"',
    '"webpack-bundle-analyzer"':'"webpack-bundle-analyzer": "^4.10.0"',
    '"zone.js"': '"zone.js": "^0.14.6"'
}

start_message = """
  xx ----------------------------------------- xx
  xx ||||||||||||||||||||||||||||||||||||||||| xx
  xx ----------------------------------------- xx
  xx | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx | xx
  xx | x                                   x | xx
  xx | x           ANGULAR 17              x | xx
  xx | x          UPGRADE TOOL             x | xx
  xx | x            PROCESS                x | xx
  xx | x            STARTED                x | xx
  xx | x                                   x | xx
  xx | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx | xx
  xx ----------------------------------------- xx
  xx ||||||||||||||||||||||||||||||||||||||||| xx
  xx ----------------------------------------- xx
  """

loading_message = """
  xx ----------------------------------------- xx
  | x                                         x |
  | x                PROCESSING               x |
  | x                                         x |
  xx ----------------------------------------- xx
  """

ncu_loading_message = """
  xx ----------------------------------------- xx
  | x                                         x |
  | x         NCU STAGE ::PROCESSING          x |
  | x                                         x |
  xx ----------------------------------------- xx
  """

def print_colored(text, color, end='\n'):
    colors = {'red': '\x1b[31m', 'green': '\x1b[32m', 'yellow': '\x1b[33m', 'blue': '\x1b[34m'}
    reset = '\x1b[0m'
    sys.stdout.write(colors.get(color, '') + text + reset + end)

def progress_bar(message: str, color: str) -> None:
  print_colored(message, color=color)
  sys.stdout.write('\r')
  for i in range(21):
      sys.stdout.write('\r')
      sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
      sys.stdout.flush()
      sleep(0.125)
  sys.stdout.write('\r')

def add_to_git_ignore() -> None:
    print_colored("ADD *.py to GITIGNORE", color="yellow")
    if os.path.exists(angular_path):
      print_colored(f"{angular_path} file exists", color="blue")
      with open(".gitignore", "a") as file:
        file.write("\n*.py\n")
        print_colored("ADDED *.py to .gitignore", color="green")
    else: print_colored(f"ANGULAR JSON DOES NOT EXIST. {angular_path}", color="red")

def git_prune() -> None:
      print_colored("PRUNE GIT ORIGIN", color="green")
      subprocess.run(["git", "remote", "prune", "origin"], check=True)

def check_master_or_main() -> str:
    print_colored("CHECKING  GIT HEAD BRANCH master OR main", color="blue")
    output = subprocess.run(["git", "ls-remote", "--symref", "origin", "HEAD"], check=True, capture_output=True, text=True)
    print_colored(f"<<<< GIT IS IN >>>> {output.stdout}", color="blue")
    if "master" in output.stdout:
      return "master"
    else:
      return "main"

def change_to_angular_upgrade_branch() -> None:
    print_colored(f"CHANGE GIT BRANCH STAGE :: creating a new branch..... {branch_name}", color="blue")
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)

def change_git() -> None:
    master_or_main = check_master_or_main()
    print_colored("-----------------------------", color="green")
    print("-------- YOUR GIT HEAD BRANCH IS IN ----------", master_or_main)
    print(master_or_main)
    print_colored("-----------------------------", color="green")
    subprocess.run(["git", "switch", master_or_main], check=True)
    print_colored("CHANGE GIT BRANCH STAGE :: pulling latest from master.....", color="blue")
    subprocess.run(["git", "pull"], check=True)
    change_to_angular_upgrade_branch()

def modify_nvm_rc() -> None:
  if os.path.exists(angular_path):
    with open(".nvmrc", "w") as file:
      file.write("20\n")

def modify_jenkins_file() -> None:
  if os.path.exists(angular_path):
    print_colored("MODIFY JENKINGS FILE :: modifying.....", color="blue")
    for key, value in jenkins_search_words.items():
       search_and_replace(jenkins_file_path, key, value)

def modify_apx_dialog() -> None:
  if os.path.exists(angular_path):
    print_colored("MODIFY APX DIALOG SERVICE PATH :: modifying.....", color="blue")
    for key, value in apx_dialog_service_words.items():
       search_and_replace_in_files(apx_dialog_service_path, key, value)

def search_and_replace(file_path, search_word, replace_word):
    print_colored("SEARCH AND REPLACE STAGE :: working on it.....", color="blue")
    try:
      with open(file_path, 'r') as file:
          file_contents = file.read()
          updated_contents = file_contents.replace(search_word, replace_word)

      with open(file_path, 'w') as file:
          file.write(updated_contents)
      print_colored(f"SEARCH AND REPLACE STAGE :: File {file_path}, replacement of {search_word}, to {replace_word} updated successfully.", color="green")

    except FileNotFoundError: print_colored(f"SEARCH AND REPLACE STAGE '{file_path}' NOT FOUND, ABORTING...", color="red")

def search_and_replace_in_files(file_path, search_word, replace_word):
    print_colored("SEARCH AND REPLACE IN FILES STAGE :: working on it.....", color="blue")
    for path, dirs, files in os.walk(file_path):
      for f in files:
        if f.endswith(".ts"):
            file_path_url = os.path.join(path, f)
            with open(file_path_url, 'r') as file:
              file_contents = file.read()
              updated_contents = file_contents.replace(search_word, replace_word)

            with open(file_path_url, 'w') as file:
                file.write(updated_contents)

    print_colored(f"SEARCH AND REPLACE IN FILES STAGE :: File {file_path}, replacement of {search_word}, to {replace_word} updated successfully.", color="green")


def change_lib_package_json_package_data() -> None:
    file_path = "projects"
    if file_path:
      print_colored("PROJECTS FOLDER FOUND :: working on it.....", color="blue")
      for path, dirs, files in os.walk(file_path):
        for f in files:
          if f == "package.json":
            file_path_url = os.path.join(path, f)
            for line in fileinput.input(file_path_url):
              line = line.rstrip()
              for key, value in fields.items():
                if key in line:
                  get_line_numbers(file_path_url, key, value)

    else:
      print_colored("NO PROJECTS FOLDER FOUND EXISTING", color="blue")

def change_nvm_and_install() -> None:
  if os.path.exists(angular_path):
    print_colored("CHANGE NVM & INSTALL NEW NODE PACKAGES :: CHANGING.....", color="blue")
    nvm_command = 'nvm use 20; npm install'
    subprocess.run(['zsh', '-i', '-c', nvm_command])
    print_colored(">>>> CHANGE NVM & INSTALL NEW NODE PACKAGES STAGE WAS SUCCESSFUL", color="green")

def correct_zone_js_path_in_polyfills() -> None:
  if os.path.exists(polyfills_path):
    with open(polyfills_path, 'r') as file:
          file_contents = file.read()
          if 'import "zone.js/dist/zone.js"' in file_contents:
            updated_contents = file_contents.replace('import "zone.js/dist/zone.js"', 'import "zone.js"')

            with open(polyfills_path, 'w') as file:
                file.write(updated_contents)
                print_colored(f"CHECKING POLYFILLS ZONE JS PATH :: STARTING..... {file_contents}", color="blue")
  print_colored("NO POLYFILLS FOUND", color="green")


def run_dev_i18n() -> None:
   nvm_command = 'nvm use 20; npm run dev-i18n'
   subprocess.run(['zsh', '-i', '-c', nvm_command])

def start_server() -> None:
  if os.path.exists(angular_path):
    print_colored("START SERVER STAGE :: STARTING.....", color="blue")
    nvm_command = 'nvm use 20; npm run start'
    subprocess.run(['zsh', '-i', '-c', nvm_command])
    print_colored("SERVER SUCCESSFULLY STARTED", color="green")

def check_current_git_branch() -> str:
    output = subprocess.run(["git", "branch", "--show-current"], check=True, capture_output=True, text=True)
    return output.stdout

def git_push_changes_to_remote() -> None:
    current_git_branch = check_current_git_branch()
    print_colored(f"PUSHING GIT CHANGES :: STARTING....., GIT HEAD IS IN {current_git_branch}", color="yellow")
    if current_git_branch == "main" or current_git_branch == "master":
      print_colored(f"GIT PUSH WAS NOT SUCCESSFUL, GIT HEAD IS IN {current_git_branch}", color="red")
    else:
      run_git_push()

def run_git_push() -> None:
    message = """
      -----------------------------------------
      | xxxxxxxxxxxx ADDING GIT xxxxxxxxxxxxx |
      -----------------------------------------
      """
    print_colored(message, color="yellow")

    subprocess.run(["git", "add", "."], check=True)
    print_colored("COMMIT GIT MESSAGE", color="blue")
    subprocess.run(["git", "commit", "-m", "feat: initial auto commit changes"], check=True)
    print_colored("GIT PUSH", color="blue")
    subprocess.run(["git", "push", "--set-upstream", "origin", branch_name, "--no-verify"], check=True)
    print_colored("GIT PUSH WAS SUCCESSFUL", color="green")

def update_angular_package_json() -> None:
    try:
      for line in fileinput.input(package_json_file_name):
        line = line.rstrip()
        for key, value in fields.items():
          if key in line:
            get_line_numbers(package_json_file_name, key, value)
      print_colored("ANGULAR JSON WAS UPDATED", color="green")

    except FileNotFoundError: print_colored("ANGULAR JSON WAS NOT UPDATED", color="red")

def get_line_numbers(filename: str, key: str, value: str) -> None:
  try:
     with open(filename, "r") as file:
        for line_number, line in enumerate(file, 1):
          if key in line:
            replace_json_lines(filename, line_number, value)
  except FileNotFoundError: print_colored("get_line_numbers WAS NOT UPDATED", color="red")

def replace_json_lines(filename:str, line_number: int, value: str) -> None:
  try:
    with open(filename, 'r') as file:
      data = file.readlines()

    if "}" not in data[line_number]:
      value = value + ","

    data[line_number - 1] = value + "\n"

    with open(filename, 'w') as file:
      file.writelines(data)
      print_colored(f"::: package.json update was successful ::: {value}", color="blue")

  except FileNotFoundError: print_colored("replace_json_lines WAS NOT SUCCESSFUL", color="red")


def prettify_project() -> None:
  if os.path.exists(angular_path):
    print_colored("FORMAT FILES:: Prettify is running.....", color="blue")
    try:
      subprocess.run(["npx", "prettier", ".", "--write"], check=True)
    except FileNotFoundError: print_colored("prettify_project WAS NOT SUCCESSFUL", color="red")


def remove_package_json() -> None:
  if os.path.exists(package_lock_delete_path):
    print_colored("DELETE PACKAGE.LOCK JSON STAGE:: Deleting package_lock.json.....", color="yellow")
    os.remove(package_lock_delete_path)
    print_colored(f">>> The file {package_lock_delete_path} has been deleted.", color="green")
  else:
    print_colored(f">>> The file {package_lock_delete_path} does not exist.", color="green")

def remove_node_modules() -> None:
  print_colored("DELETE NODE MODULES :: deleting node_modules.....", color="blue")
  if os.path.exists(node_modules_delete_path):
    shutil.rmtree(node_modules_delete_path)
    print_colored(f">>> The directory {node_modules_delete_path} has been deleted.", color="yellow")
  else:
    print_colored(f">>> The directory {node_modules_delete_path} does not exist.", color="green")

def remove_old_files() -> None:
    remove_package_json()
    remove_node_modules()

def replace_browser_target() -> None:
    print_colored("REPLACE browserTarget TO buildTarget", color="blue")
    if os.path.exists(angular_path):
      search_and_replace(angular_path, '"browserTarget"', '"buildTarget"')
      print_colored("buildTarget replacement has been successful in angular.json.", color="green")
    else:
      print_colored("ANGULAR JSON DOES NOT EXIST.", color="red")

def delete_ngcc() -> None:
    print_colored("DELETING ngcc.config.js", color="blue")
    file_path = "ngcc.config.js"
    try:
      os.remove(file_path)
      print_colored(f"File '{file_path}' deleted successfully.", color="green")
    except FileNotFoundError: print_colored(f"File '{file_path}' not found.", color="yellow")

def cleanup_package_json() -> None:
  print_colored("CLEAN UP PACKAGE JSON STAGE", color="blue")
  try:
    print_colored("cleaning up.....", color="yellow")
    search_and_replace(package_json_file_name, '"node": ">=16"', '"node": ">=20"')
    search_and_replace(package_json_file_name, '"npm": ">=8"', '"npm": ">=10"')
    search_and_replace(package_json_file_name, 'husky install', 'husky')
  except FileNotFoundError: print_colored("clean up package json WAS NOT SUCCESSFUL", color="red")

def delete_postinstall() -> None:
  try:
    with open(package_json_file_name, "r") as file:
      for line_number, line_item in enumerate(file, 1):
        if "ngcc --" in line_item:
          replace_ngcc(line_number - 1)
  except FileNotFoundError: print_colored("prettify_project WAS NOT SUCCESSFUL", color="red")

def replace_ngcc(line_number: int) -> None:
  try:
    with open(package_json_file_name, "r") as file:
      data = file.readlines()

    with open(package_json_file_name, 'w') as file:
              for number, line in enumerate(data):
                  if number != line_number:
                      file.write(line)
    print_colored("::: package.json ngcc remove update was successful :::", color="green")
  except FileNotFoundError: print_colored("prettify_project WAS NOT SUCCESSFUL", color="red")

def ncu_package_install() -> None:
  if os.path.exists(angular_path):
    npm_list = subprocess.run(["npm", "list", "-g", "--depth=0"], check=True, capture_output=True, text=True)
    if "npm-check-updates" in npm_list.stdout:
        print_colored("npm-check-updates detected, skipping the step", color="yellow")
    else:
        print_colored("No npm-check-updates detected, installing", color="blue")
        subprocess.run(["npm", "install", "-g", "npm-check-updates"], check=True)
    print_colored("::: NCU Check stage :: was successful :::", color="green")
  else:
      print_colored("ANGULAR JSON DOES NOT EXIST.", color="red")

def ncu_check_nable_packages() -> None:
  if os.path.exists(angular_path):
    print_colored(">>>> NCU Check n-able package stage:: installing ncu package.....", color="blue")
    subprocess.run([
       "ncu", "-x",
       "/@angular.*$/", "-x",
       "typescript", "-x",
       "@apollo/client", "-x",
       "angular-gridster2", "-x",
       "apollo-angular", "-x",
       "devextreme", "-x",
       "devextreme-angular", "-x",
       "eslint", "-x",
       "ng-packagr", "-x",
       "rxjs", "-x",
       "graphql", "-x",
       "odata-query", "-x",
       "zone.js", "-x",
       "angular-in-memory-web-api", "-x",
       "@n-able/msp-rmm-test-automation-lib", "-x",
       "@n-able/atoms", "-u"], check=True)
    print_colored("::: NCU Check n-able package stage :::", color="green")
  else:
      print_colored("ANGULAR JSON DOES NOT EXIST.", color="red")

def ncu_check_packages() -> None:
    ncu_package_install()
    ncu_check_nable_packages()

def main() -> None:
    progress_bar(start_message, "green")
    add_to_git_ignore()
    git_prune()
    change_git()
    remove_old_files()
    progress_bar(loading_message, "blue")
    cleanup_package_json()
    update_angular_package_json()
    progress_bar(loading_message, "blue")
    ncu_check_packages()
    modify_nvm_rc()
    progress_bar(loading_message, "blue")
    modify_jenkins_file()
    modify_apx_dialog()
    replace_browser_target()
    progress_bar(loading_message, "blue")
    delete_ngcc()
    delete_postinstall()
    progress_bar(loading_message, "blue")
    correct_zone_js_path_in_polyfills()
    run_dev_i18n()
    progress_bar(loading_message, "blue")
    progress_bar(loading_message, "green")
    change_nvm_and_install()
    progress_bar(loading_message, "blue")
    change_lib_package_json_package_data()
    prettify_project()
    progress_bar(loading_message, "blue")
    start_server()
    git_push_changes_to_remote()

if __name__ == "__main__":
    main()
