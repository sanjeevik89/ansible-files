#!/usr/bin/python3

"""

     Revision history:
     24 Sep 2020  |  1.0 - initial release

"""

DOCUMENTATION = '''
---
module: hjson_to_json.py
author: Sanjeevi Kumar, Wipro Technologies
version_added: "1.0"
short_description: Read an .hjson file and output JSON
description:
    - Read the HJON file specified and output JSON file
 
requirements:
    - The hjson Python module must be installed on the Ansible host. This can be installed using pip:
      sudo pip install hjson  

options:
    input:
        description:
            - The name with location of the HJSON file
        required: true
    output:
        description:
            - The name with location of the JSON file
        required: true    
'''

EXAMPLES = '''

    Running the module from the command line:

      ansible localhost -m hjson_to_json -a input="/tmp/sample.hjson" -a output="/tmp/sample.json" -M ~/ansible/library
   

    In a playbook configuration, given a host entry:
      

      $ cat hjson_to_json.yml
      ---
      - name: Test playbook to convert hjson to json
        hosts: localhost

        roles:
          - {role: hjson_to_json, debug: on}


      $ ansible-playbook hjson_to_json.yml -e "input_file='/tmp/sample.hjson'" -e "output_file='/tmp/sample.json'"

'''
import hjson

# ---------------------------------------------------------------------------
# convert hjson to json
# ---------------------------------------------------------------------------

def hjson_to_json(input_file,output_file):
    "Read the HJSON file and return as JSON"    
    try:
        with open(input_file) as infile:
            data = hjson.loads(infile.read())
            print(data)
        with open(output_file, 'w') as outfile:
            json.dump(data, outfile)        
    except IOError:
        return (1, "IOError on input file:%s" % input_file)

    return (0, data)

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    " Read parameters and add common file arguments "
    module = AnsibleModule(argument_spec = dict(
             input = dict(required=True),
             output = dict(required=True)
             ),
             check_invalid_arguments=False,
             add_file_common_args=True)
    code, response = hjson_to_json(module.params["input"],module.params["output"])
    if code == 1:
        module.fail_json(msg=response)
    else:
        module.exit_json(**response)

    return code


from ansible.module_utils.basic import *
main()
#
