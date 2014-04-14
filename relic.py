from jinja2 import Environment, FileSystemLoader
from clint import arguments
import os
import json

# Get demands
args = arguments.Args()
demands_filename = args.get(0)
demands_file = open(demands_filename)
demands_lines = demands_file.readlines()
try:
    demands = json.loads(demands_lines)
except Exception, e:
    print e
    print demands_lines
    print "Could not parse demands."


# Set up law
env = Environment(loader=FileSystemLoader(''))
template = env.get_template('default_resolution.html')
output_from_parsed_template = template.render(demands)
print output_from_parsed_template

# Write the law
with open(demands_filename.replace('.html', '.txt'), "wb") as fh:
        fh.write(output_from_parsed_template)
