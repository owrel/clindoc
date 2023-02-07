
# %%
from clindoc import Clindoc
# Test 1 - Classic
print("Test 1 - Classic")
c = Clindoc({'src_dir': 'examples/mapf'})
c.build_documentation()
print()

# %% Test 2 - Excluding dependency graph and source files
from clindoc import Clindoc

print("Test 2 - Excluding dependency graph and source files")
c = Clindoc({'src_dir': 'examples/mapf',
            'dependencygraph': {'exclude': True}, 'source': {'exclude': True}})
c.build_documentation()
print()

# %% Test 3 - Excluding specific source files
from clindoc import Clindoc

print("Test 3 - Excluding specific source files")
c = Clindoc({'src_dir': 'examples/mapf',
            'source': {'exclude_file': ['examples/mapf/input.lp.lp']}})
c.build_documentation()
print()
# %% Test 4 - Custom project name and description
print("Test 4 - Custom project name and description")
c = Clindoc({'src_dir': 'examples/mapf', 'project_name': 'Mapf Project',
            'description': 'This is an example project for testing clindoc'})
c.build_documentation()
print()

# %% Test 5 - Contributor documentation with custom options
from clindoc import Clindoc

print("Test 5 - Contributor documentation with custom options")
c = Clindoc({'src_dir': 'examples/mapf',
            'contributordoc': {'hide_code': True, 'group_by': 'type'}})
c.build_documentation()
print()

# %% Test 6 - Dependency graph with custom format
from clindoc import Clindoc
print("Test 6 - Dependency graph with custom format")
c = Clindoc({'src_dir': 'examples/mapf', 'dependencygraph': {'format': 'png'}})
c.build_documentation()
print()

# %% Test 7 - No src_dir specified
import os
from clindoc import Clindoc
print("Test 7 - No src_dir specified")
os.chdir('examples/')
c = Clindoc()
c.build_documentation()
os.chdir('..')
print()


# %% Test 8 - Using 'examples/sudoku' as src_dir
from clindoc import Clindoc

print("Test 8 - Using 'examples/sudoku' as src_dir")
c = Clindoc({'src_dir': 'examples/sudoku'})
c.build_documentation()

# %% Test 9 - Using custom output directories
print("Test 9 - Using custom output directories")
c = Clindoc({'src_dir': 'examples/mapf', 'doc_dir': 'examples/mapf/mapf_docs',
            'out_dir': 'examples/mapf/mapf_build'})
c.build_documentation()
print()


# %% Test 10-11 - Dumping a configuration file & Using a configuration file
from clindoc import Clindoc
print("Test 11 - Dumping a configuration file")
c = Clindoc({'src_dir': 'examples/mapf', 'project_name': 'Mapf Project',
            'description': 'This is an example project for testing clindoc', 'dump_conf': 'examples/config.json', 'doc_dir' : 'examples/hello', 'out_dir' : 'examples/hello/out'})
c.build_documentation()
print()

#%%
print("Test 10 - Using a configuration file")
c = Clindoc({'conf_path': 'examples/config.json'})
c.build_documentation()
print()

# %%
