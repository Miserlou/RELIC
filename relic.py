#! /usr/bin/python

from jinja2 import Environment, FileSystemLoader
from clint import arguments
import os
import json

# Get demands
args = arguments.Args()
demands_filename = args.get(0)
with open(demands_filename, "r") as demands_file:
    demands_lines=demands_file.read().replace('\n', '')

try:
    demands = json.loads(demands_lines)
    print json.dumps(demands, indent=4)
except Exception, e:
    print e
    print demands_lines
    print "Could not parse demands."


# Set up law
env = Environment(loader=FileSystemLoader(''))
template = env.get_template('default_resolution.law')
output_from_parsed_template = template.render(demands)
print output_from_parsed_template

# Write the law
with open(demands_filename.replace('.demands', '.txt'), "wb") as fh:
        fh.write(output_from_parsed_template)
