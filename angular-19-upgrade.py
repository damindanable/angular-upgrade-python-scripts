import fileinput
import subprocess
import os
import shutil
import sys
from time import sleep
import random
import re
# from tqdm import tqdm

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
node_version = "20.18\n"
jenkins_search_words = {
 'quasar@release/v13': 'quasar@release/v14',
 'nodeVersion: 16': 'nodeVersion: 20'
}
apx_dialog_service_path = f"{folder_path}"
# projects_path = f"{folder_path}/projects/msp-monitored-devices/src/lib/"
projects_path = f"{folder_path}/projects/"
src_path = f"{folder_path}/src/"
apx_dialog_service_words = {
 '@n-able/neb-common/apx-confirmation-dialog': '@n-able/neb-common/apx-dialog',
}

apx_common_import = {
 'import { ApxCommonModule } from "@n-able/apex-ui";': 'import { ApxCommonModule } from "@n-able/apx-common";',
}

fields = {
    '"angular-in-memory-web-api"': '"angular-in-memory-web-api": "^0.19.0"',
    '"@angular/animations"': '"@angular/animations": "^19.2.11"',
    '"@angular/common"':'"@angular/common": "^19.2.11"',
    '"@angular/core"':'"@angular/core": "^19.2.11"',
    '"@angular/forms"':'"@angular/forms": "^19.2.11"',
    '"@angular/localize"':'"@angular/localize": "^19.2.11"',
    '"@angular/platform-browser"':'"@angular/platform-browser": "^19.2.11"',
    '"@angular/platform-browser-dynamic"':'"@angular/platform-browser-dynamic": "^19.2.11"',
    '"@angular/router"':'"@angular/router": "^19.2.11"',
    '"@angular-devkit/architect"':'"@angular-devkit/architect": "^0.1902.12"',
    '"@angular-devkit/build-angular"':'"@angular-devkit/build-angular": "^19.2.12"',
    '"@angular-devkit/core"':'"@angular-devkit/core": "^19.2.12"',
    '"@angular-eslint/builder"':'"@angular-eslint/builder": "^19.3.0"',
    '"@n-able/xliff-tools"':'"@n-able/xliff-tools": "^12.0.2"',
    '"@n-able/qsr-devkit': '"@n-able/qsr-devkit": "^5.0.2"',
    '"@ngneat/spectator"':'"@ngneat/spectator": "^19.5.0"',
    '"@angular-eslint/eslint-plugin"':'"@angular-eslint/eslint-plugin": "^19.3.0"',
    '"@angular-eslint/eslint-plugin-template"':'"@angular-eslint/eslint-plugin-template": "^19.3.0"',
    '"@angular-eslint/schematics"':'"@angular-eslint/schematics": "^19.3.0"',
    '"@angular-eslint/template-parser"':'"@angular-eslint/template-parser": "^19.3.0"',
    '"@angular/cdk"':'"@angular/cdk": "^19.2.11"',
    '"@angular/cli"':'"@angular/cli": "^19.2.12"',
    '"@angular/compiler"':'"@angular/compiler": "^19.2.11"',
    '"@angular/compiler-cli"':'"@angular/compiler-cli": "^19.2.11"',
    '"@angular/language-service"':'"@angular/language-service": "^19.2.11"',
    '"@apollo/client"':'"@apollo/client": "^3.13.8"',
    '"ng-packagr"':'"ng-packagr": "^19.2.2"',
    '"angular-gridster2"':'"angular-gridster2": "^19.0.0"',
    '"angular-oauth2-oidc"':'"angular-oauth2-oidc": "^19.0.0"',
    '"apollo-angular"':'"apollo-angular": "^10.0.3"',
    '"devextreme"':'"devextreme": "24.2.6"',
    '"devextreme-angular"':'"devextreme-angular": "24.2.6"',
    '"rxjs"':'"rxjs": "7.8.2"',
    '"moment-timezone"': '"moment-timezone": "0.5.46"',
    '"@ngtools/webpack"':'"@ngtools/webpack": "^19.2.12"',
    '"webpack-dev-server"':'"webpack-dev-server": "^4.15.2"',
    '"tailwindcss"':'"tailwindcss": "^3.4.1"',
    '"@n-able/qsr-api-client"':'"@n-able/qsr-api-client": "^21.0.0"',
    '"@n-able/apx-product-bar"':'"@n-able/apx-product-bar": "17.0.1"',
    '"graphql"': '"graphql": "^16.11.0"',
    '"eslint"':'"eslint": "8.57.1"',
    '"@n-able/es-lint-rules"':'"@n-able/es-lint-rules": "5.0.3"',
    '"@n-able/apx-nav-menu"':'"@n-able/apx-nav-menu": "^15.0.0"',
    '"@n-able/qsr-sso"':'"@n-able/qsr-sso": "^7.0.0"',
    '"odata-query"':'"odata-query": "^7.0.9"',
    '"typescript"':'"typescript": "~5.5.4"',
    '"webpack-bundle-analyzer"':'"webpack-bundle-analyzer": "^4.10.0"',
    '"zone.js"': '"zone.js": "^0.15.0"',
    '"@storybook/addons"': '"@storybook/addons": "7.6.20"',
    '"@storybook/addon-a11y"': '"@storybook/addon-a11y": "8.6.12"',
    '"@storybook/addon-actions"': '"@storybook/addon-actions": "8.6.12"',
    '"@storybook/addon-controls"': '"@storybook/addon-controls": "8.6.12"',
    '"@storybook/addon-controls"': '"@storybook/addon-controls": "8.6.12"',
    '"@storybook/addon-docs"': '"@storybook/addon-docs": "8.6.12"',
    '"@storybook/addon-essentials"': '"@storybook/addon-essentials": "8.6.12"',
    '"@storybook/addon-interactions"': '"@storybook/addon-interactions": "8.6.12"',
    '"@storybook/addon-links"': '"@storybook/addon-links": "8.6.12"',
    '"@storybook/addon-mdx-gfm"': '"@storybook/addon-mdx-gfm": "8.6.12"',
    '"@storybook/angular"': '"@storybook/angular": "8.6.12"',
    '"@storybook/blocks"': '"@storybook/blocks": "8.6.12"',
    '"@storybook/manager-api"': '"@storybook/manager-api": "8.6.12"',
    '"@storybook/test"': '"@storybook/test": "8.6.12"',
    '"@storybook/test-runner"': '"@storybook/test-runner": "^0.22.0"',
    '"@storybook/theming"': '"@storybook/theming": "8.6.12"',
    '"@storybook/types"': '"@storybook/types": "8.6.12"',
    '"@storybook/builder-webpack5"': '"@storybook/builder-webpack5": "8.6.12"',
    '"storybook"': '"storybook": "8.6.12"',
    '"storybook-addon-tag-badges"': '"storybook-addon-tag-badges": "1.4.0"',
    '"storybook-dark-mode"': '"storybook-dark-mode": "4.0.2"',
    '"@etchteam/storybook-addon-status"': '"@etchteam/storybook-addon-status": "5.0.0"',
    '"eslint-plugin-storybook"': '"eslint-plugin-storybook": "0.12.0"',
}

start_message = """
  xx ----------------------------------------- xx
  xx ||||||||||||||||||||||||||||||||||||||||| xx
  xx ----------------------------------------- xx
  xx | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx | xx
  xx | x                                   x | xx
  xx | x           ANGULAR 19              x | xx
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


# def progress_bar_new(message: str, color: str) -> None:
#   for i in tqdm(range(0, 50)):
#       sleep(0.125)

def progress_bar(message: str, color: str) -> None:
  print_colored(message, color=color)
  sys.stdout.write('\r')
  for i in range(21):
      sys.stdout.write('\r')
      sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
      sys.stdout.flush()
      sleep(0.125)
  sys.stdout.write('\r')

def install_ng_19() -> None:
    print_colored("INSTALLING ANGULAR 19", color="blue")
    nvm_command = 'nvm use 20; npm i -g @angular/cli@19.0.0'
    subprocess.run(['zsh', '-i', '-c', nvm_command])
    print_colored("ANGULAR 19 WAS INSTALLED SUCCESSFULLY", color="green")

def install_apex_ui_package() -> None:
    print_colored("INSTALLING APEX UI", color="blue")
    nvm_command = 'ng add @n-able/apex-ui'
    subprocess.run(['zsh', '-i', '-c', nvm_command])
    print_colored("INSTALLING APEX UI", color="green")

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
    print_colored("--------------------------------------------------------------", color="green")
    print(f"|| -------- YOUR GIT HEAD BRANCH IS IN -- {master_or_main} ---------- ||")
    print_colored("--------------------------------------------------------------", color="green")
    subprocess.run(["git", "switch", master_or_main], check=True)
    print_colored("CHANGE GIT BRANCH STAGE :: pulling latest from master.....", color="blue")
    subprocess.run(["git", "pull"], check=True)
    change_to_angular_upgrade_branch()

def modify_nvm_rc() -> None:
  if os.path.exists(angular_path):
    with open(".nvmrc", "w") as file:
      file.write(node_version)

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


def add_apx_common_imports_back() -> None:
  try:
    if os.path.exists(package_json_file_name):
      for key, value in apx_common_import.items():
       search_and_replace_in_files(folder_path, key, value)


  except FileNotFoundError: print_colored(f"APX COMMON IMPORT BACK WAS NOT SUCCESSFUL", color="red")




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
  else:
    print_colored("THERE WAS AN ERROR WHILE INSTALLING PACKAGES, UNABLE TO OPEN LOCAL SERVER", color="red")

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
    except subprocess.CalledProcessError as error:
      output = error.output
      print_colored(f"|||||| xxxxx PRETTIFY STEP WAS NOT SUCCESSFUL ERROR IN ONE OR MORE FILES xxxxxxx ||||||| {output}", color="red")


def remove_package_json() -> None:
  if os.path.exists(package_lock_delete_path):
    print_colored("DELETE PACKAGE.LOCK JSON STAGE:: Deleting package_lock.json.....", color="yellow")
    os.remove(package_lock_delete_path)
    print_colored(f">>> The file {package_lock_delete_path} has been deleted.", color="green")
  else:
    print_colored(f">>> The file {package_lock_delete_path} does not exist.", color="green")

def remove_node_modules() -> None:
  print_colored("DELETE NODE MODULES :: deleting node_modules.....", color="blue")
  sys.stdout.write('\r')
  for i in range(21):
      sys.stdout.write('\r')
      sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
      sys.stdout.flush()
      sleep(0.125)
  sys.stdout.write('\r')
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

def convert_to_es_build() -> None:
    print_colored("CONVERT TO ES BUILD", color="blue")
    if os.path.exists(angular_path):
      search_and_replace(angular_path, '"@angular-devkit/build-angular"', '"@angular/build"')
      print_colored("CONVERT TO ES BUILD has been successful in angular.json.", color="green")
    else:
      print_colored("ANGULAR JSON DOES NOT EXIST.", color="red")


def replace_angular_19_tags() -> None:
   for path, dirs, files in os.walk(folder_path):
      for file in files:
        file_path_url = os.path.join(path, file)
        standalone_text = 'standalone: false,'
        if file.endswith(".component.ts") or file.endswith(".directive.ts") or file.endswith(".pipe.ts"):
          print_colored(f"..... PATH ..... {file_path_url}", color="green")
          add_standalone_in_to_directives(file_path_url, standalone_text)
          add_standalone_in_component(file_path_url, standalone_text)
          add_standalone_in_to_pipes(file_path_url, standalone_text)


def add_standalone_in_to_directives(path: str, standalone_text: str) -> None:
  try:
    with open(path, "r") as file:
      file_contents = file.read()
      search_string_first_part = "@Directive({"
      search_string_end_part = "})"
      search_string_first_part_escaped = str(re.escape(search_string_first_part))
      search_string_end_part_escaped = str(re.escape(search_string_end_part))
      match_strings = re.findall(f"{search_string_first_part_escaped}(.*?){search_string_end_part_escaped}", file_contents, re.S)
      for string in match_strings:
          selector_string = re.findall('selector: "([^"]*)"', string)
          if selector_string:
            replace_selector_with_standalone(selector_string, path, standalone_text)
          else:
             print_colored(f"NO SELECTOR FOUND IN DIRECTIVE {path}", color="red")

  except FileNotFoundError: print_colored("replace_create_spy_obj WAS NOT SUCCESSFUL", color="red")

def add_standalone_in_to_pipes(path: str, standalone_text: str) -> None:
  try:
    with open(path, "r") as file:
      file_contents = file.read()
      search_string_first_part = "@Pipe({"
      search_string_end_part = "})"
      search_string_first_part_escaped = str(re.escape(search_string_first_part))
      search_string_end_part_escaped = str(re.escape(search_string_end_part))
      match_strings = re.findall(f"{search_string_first_part_escaped}(.*?){search_string_end_part_escaped}", file_contents, re.S)

      for string in match_strings:
          one_line_string = f"{search_string_first_part}{string}{search_string_end_part}"
          line_numbers = len(one_line_string.split("\n"))

          selector_string = re.findall('name: "([^"]*)"', string)
          if line_numbers == 1:
            one_line_string_replacement = f"{search_string_first_part}{string}, {standalone_text}{search_string_end_part}"
            with open(path, 'r') as file:
                file_contents = file.read()
                updated_on_line_pipe_contents = file_contents.replace(one_line_string, one_line_string_replacement)

            with open(path, 'w') as file:
                file.write(updated_on_line_pipe_contents)

          elif selector_string:
              selector_input_converted_brackets = str(selector_string).replace("['", "").replace("']", "")
              converted_string = str(selector_input_converted_brackets).replace("'", '').replace("'", "")
              selector = 'name: "' + converted_string + '"'

              line_number = common_get_line_number(selector, path)

              with open(path, 'r') as ReadFileData:
                if line_number is not None:
                  data = ReadFileData.readlines()
                  data.insert(line_number, standalone_text)

                  with open(path, 'w') as FileWriteData:
                    FileWriteData.writelines(data)

  except FileNotFoundError: print_colored("replace_create_spy_obj WAS NOT SUCCESSFUL", color="red")

def add_standalone_in_component(path: str, standalone_text: str) -> None:
  try:
    with open(path, "r") as file:
      file_contents = file.read()
      search_string_first_part = "@Component({"
      search_string_end_part = "})"
      search_string_first_part_escaped = str(re.escape(search_string_first_part))
      search_string_end_part_escaped = str(re.escape(search_string_end_part))
      match_strings = re.findall(f"{search_string_first_part_escaped}(.*?){search_string_end_part_escaped}", file_contents, re.S)

      for string in match_strings:
          selector_string = re.findall('selector: "([^"]*)"', string)
          template_string = re.findall('templateUrl: "([^"]*)"', string)
          if selector_string:
            replace_selector_with_standalone(selector_string, path, standalone_text)

          elif template_string:
            print_colored(f"NO SELECTOR FOUND IN COMPONENT {path}", color="red")
            template_string_converted_brackets = str(template_string).replace("['", "").replace("']", "")
            template_converted_string = str(template_string_converted_brackets).replace("'", '').replace("'", "")
            template_selector = 'templateUrl: "' + template_converted_string + '",'
            template_replace_word = template_selector + " " + standalone_text
            with open(path, 'r') as ReadFileData:
                template_data = ReadFileData.read()
                template_updated_contents = template_data.replace(template_selector, template_replace_word)

                with open(path, 'w') as FileWriteData:
                  FileWriteData.writelines(template_updated_contents)

  except FileNotFoundError: print_colored("replace_create_spy_obj WAS NOT SUCCESSFUL", color="red")


def replace_selector_with_standalone(selector_string: str, path: str, standalone_text: str) -> None:
  selector_input_converted_brackets = str(selector_string).replace("['", "").replace("']", "")
  converted_string = str(selector_input_converted_brackets).replace("'", '').replace("'", "")
  selector = 'selector: "' + converted_string + '",'
  replace_word = selector + " " + standalone_text
  with open(path, 'r') as ReadFileData:
    data = ReadFileData.read()
    updated_contents = data.replace(selector, replace_word)

  with open(path, 'w') as FileWriteData:
    FileWriteData.writelines(updated_contents)

def add_standalone_in_to_component(path: str, line_number: int, standalone_text: str) -> None:
  try:

    with open(path, "r") as file:
      file_contents = file.read()
      search_string_first_part = "@Component({"
      search_string_end_part = "})"
      search_string_first_part_escaped = str(re.escape(search_string_first_part))
      search_string_end_part_escaped = str(re.escape(search_string_end_part))
      match_strings = re.findall(f"{search_string_first_part_escaped}(.*?){search_string_end_part_escaped}", file_contents, re.S)

      for string in match_strings:
          if "standalone" not in string:
            with open(path, 'r') as ReadFileData:
              data = ReadFileData.readlines()
              data.insert(line_number, standalone_text)

            with open(path, 'w') as FileWriteData:
              FileWriteData.writelines(data)


  except FileNotFoundError: print_colored("replace_create_spy_obj WAS NOT SUCCESSFUL", color="red")


def common_get_line_number(text: str, path: str) -> int:
  try:

    with open(path, "r") as file:
      for line_number, line_item in enumerate(file):
        if text in line_item:
          return line_number + 1
  except FileNotFoundError: print_colored("--- exception in common_get_line_number ---", color="red")

def remove_default_project() -> None:
  print_colored("REMOVE defaultProject from angular.json", color="blue")
  if os.path.exists(angular_path):
    with open(angular_path, "r") as f:
        lines = f.readlines()
    with open(angular_path, "w") as f:
        for line in lines:
            if '"defaultProject"' not in line:
                f.write(line)

def delete_ngcc() -> None:
    print_colored("DELETE ngcc.config.js", color="blue")
    file_path = "ngcc.config.js"
    try:
      os.remove(file_path)
      print_colored(f"File '{file_path}' deleted successfully.", color="green")
    except FileNotFoundError: print_colored(f"File '{file_path}' not found.", color="yellow")

def cleanup_package_json() -> None:
  print_colored("CLEAN UP PACKAGE JSON STAGE", color="blue")
  try:
    print_colored("....... CLEANING UP .....", color="yellow")
    search_and_replace(package_json_file_name, '"node": ">=16"', '"node": ">=20"')
    search_and_replace(package_json_file_name, '"npm": ">=8"', '"npm": ">=10"')
    search_and_replace(package_json_file_name, 'husky install', 'husky')
  except FileNotFoundError: print_colored("clean up package json WAS NOT SUCCESSFUL", color="red")

def add_storybook_if_not_available() -> None:
  print_colored("CHECKING STORYBOOK IN PACKAGE JSON", color="blue")
  try:
    with open(package_json_file_name, "r") as file:

        file_contents = file.read()
        search_string_first_part = '"@storybook/'
        search_string_end_part = ','
        search_string_first_part_escaped = str(re.escape(search_string_first_part))
        search_string_end_part_escaped = str(re.escape(search_string_end_part))
        match_strings = re.findall(f"{search_string_first_part_escaped}(.*?){search_string_end_part_escaped}", file_contents, re.S)

        if len(match_strings) > 0:
            line_number = common_get_line_number(match_strings[1], package_json_file_name)
            search_string_story_book_first_part = '"storybook": '
            search_string_story_book_end_part = ','
            search_string_story_book_first_part_escaped = str(re.escape(search_string_story_book_first_part))
            search_string_story_book_end_part_escaped = str(re.escape(search_string_story_book_end_part))
            match_strings = re.findall(f"{search_string_story_book_first_part_escaped}(.*?){search_string_story_book_end_part_escaped}", file_contents, re.S)
            converted_brackets = str(match_strings).replace("['", "").replace("']", "")
            converted_string = str(converted_brackets).replace("'", '').replace("'", "")
            if "8." not in converted_string:
                print_colored(f"NO STORYBOOK FOUND ADDING STORYBOOK TO PACKAGE.JSON {converted_string} ", color="red")
                standalone_text = '"storybook": "8.6.12",\n'
                with open(package_json_file_name, 'r') as ReadFileData:
                  data = ReadFileData.readlines()
                  data.insert(line_number, standalone_text)

                with open(package_json_file_name, 'w') as FileWriteData:
                  FileWriteData.writelines(data)
        else:
          print_colored("@storybook does not exist, skipping storybook check", color="yellow")
          return
  except FileNotFoundError: print_colored("STORYBOOK IN PACKAGE JSON WAS NOT SUCCESSFUL", color="red")

def delete_postinstall() -> None:
  try:
    with open(package_json_file_name, "r") as file:
      for line_number, line_item in enumerate(file, 1):
        if "ngcc --" in line_item:
          replace_ngcc(line_number - 1)
  except FileNotFoundError: print_colored("DELETE POST INSTALL STEP WAS NOT SUCCESSFUL", color="red")

def replace_ngcc(line_number: int) -> None:
  try:
    with open(package_json_file_name, "r") as file:
      data = file.readlines()

    with open(package_json_file_name, 'w') as file:
              for number, line in enumerate(data):
                  if number != line_number:
                      file.write(line)
    print_colored("::: package.json ngcc remove update was successful :::", color="green")
  except FileNotFoundError: print_colored("REPLACE NGCC STEP WAS NOT SUCCESSFUL", color="red")

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
      "/@angular-.*$/", "-x",
      "/@storybook.*$/", "-x",
      "/@storybook-.*$/", "-x",
      "storybook", "-x",
      "/storybook-*$/", "-x",
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
      "@ngtools/webpack", "-x",
      "odata-query", "-x",
      "zone.js", "-x",
      "tailwindcss", "-x",
      "moment-timezone", "-x",
      "webpack-dev-server", "-x",
      "angular-in-memory-web-api", "-x",
      "angular-oauth2-oidc", "-x",
      "@n-able/qsr-api-client", "-x",
      "@n-able/msp-rmm-test-automation-lib", "-x",
      "@n-able/xliff-tools", "-x",
      "@ngneat/spectator", "-x",
      "@n-able/es-lint-rules", "-x",
      "@n-able/apx-nav-menu", "-x",
      "@n-able/apx-product-bar", "-x",
      "@n-able/qsr-sso", "-x",
      "@n-able/qsr-devkit", "-x",
      "eslint-plugin-storybook", "-x",
      "@etchteam/storybook-addon-status", "-x",
      "@n-able/atoms", "-u"], check=True)
    print_colored("::: NCU Check n-able package stage :::", color="green")
  else:
      print_colored("ANGULAR JSON DOES NOT EXIST.", color="red")

def ncu_check_packages() -> None:
    ncu_package_install()
    ncu_check_nable_packages()

def main() -> None:
    progress_bar(start_message, "green")
    # git_prune()
    # change_git()
    install_ng_19()
    add_to_git_ignore()
    remove_old_files()
    add_storybook_if_not_available()
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
    remove_default_project()
    convert_to_es_build()
    replace_angular_19_tags()
    progress_bar(loading_message, "blue")
    delete_ngcc()
    delete_postinstall()
    progress_bar(loading_message, "blue")
    correct_zone_js_path_in_polyfills()
    run_dev_i18n()
    progress_bar(loading_message, "blue")
    change_nvm_and_install()
    progress_bar(loading_message, "blue")
    install_apex_ui_package()
    progress_bar(loading_message, "blue")
    change_lib_package_json_package_data()
    add_apx_common_imports_back()
    prettify_project()
    progress_bar(loading_message, "blue")
    start_server()
    git_push_changes_to_remote()

if __name__ == "__main__":
    main()
