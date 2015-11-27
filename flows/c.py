import flowtils as u

extensions = ["c"]

def run(**kw):
    project_file_contents = u.get_file(kw, ".project")
    if project_file_contents:
        u.tmux_shell("cd %s; %s" % (kw.get("basepath"), project_file_contents), session = "temp", pane = 0)
        return

    command = "gcc %s; ./a.out" % kw.get("filepath")
    u.shell(command, **kw)

