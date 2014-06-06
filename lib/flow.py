import vim
import os
import imp
import glob
import modules
import re
import flowtils
import flowconfig

filelock = None

def run(method = "run"):

    # update flow configuration
    flowconfig.update()

    # make sure to normalize, as <n-args> passes an empty string if no args
    if not method:
        method = "run"

    # generate file information to be passed around as kwargs
    filepath = _get_file_path()
    attrs = flowtils.get_path_attributes(filepath)

    # find the correct module 
    module = _get_module(**attrs)

    if not module or not hasattr(module, method):
        print "No %s method available for this filepath" % method
        return

    # call method
    getattr(module, method)(**attrs)

def lock():
    
    global filelock
    if not filelock:
        filelock = _get_file_path()
        print "File locked"
    else:
        filelock = None
        print "File lock released"

def tmux(command):

    flowtils.tmux_shell(command)

def _get_file_path():

    global filelock
    if filelock:
        return filelock
    return vim.current.buffer.name

# **kwargs is a hash from flowtils.get_path_attributes
def _get_module(**kw):

    flows = modules.modules()

    # you can override the command in any file
    if flows.get("command").has_command(**kw):
        return flows.get("command")

    # check for flowfile
    if flows.get("flowfile").has_flowfile(**kw):
        return flows.get("flowfile")

    # check all modules
    for module_name, module in flows.iteritems():
        # check against extension
        if kw.get("extension") and hasattr(module, "extensions") and kw.get("extension") in module.extensions:
            return module
        # check if its a registered filename, for instance Gemfile or Rakefile (ruby)
        if hasattr(module, "filenames") and kw.get("filename") in module.filenames:
            return module
    
    # no module available, call the shell module
    if flows.get("anonymous").has_shebang(kw.get("filepath")):
        return flows.get("anonymous")

    return None


