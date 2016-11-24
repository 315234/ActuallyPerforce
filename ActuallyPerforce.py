import sublime
import sublime_plugin

import os.path
from subprocess import Popen, PIPE, STDOUT

# Takes one argument "text" and inserts it at the end of the current view
class NewFileContentSetter(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        self.view.insert(edit, self.view.size(), kwargs["text"])
# Wrapper for NewFileContentSetter
def append_to_view(view, text):
    view.run_command("new_file_content_setter", {"text":text})


# stupid callback after getting password
def post_password(p4passwd, command, dirname):
    p4bin = sublime.active_window().active_view().settings().get("p4", "p4")
    full_cmd = [p4bin] + command

    v = sublime.active_window().create_output_panel("Perforce")
    # v.set_read_only(False)
    # append_to_view(v, str(full_cmd) + "\n")
    append_to_view(v, "dirname = {}\n".format(dirname))
    append_to_view(v, "command = {}\n".format(" ".join(full_cmd)))

    try:
        p = Popen(  full_cmd,
                    stdout=PIPE,
                    stderr=STDOUT, # correctly interleave
                    # shell=True,
                    cwd=dirname
        )
    except FileNotFoundError as e:
        sublime.message_dialog("Popen error: " + str(e))

    stdout_data, stderr_data = p.communicate()

    if stdout_data:
        append_to_view(v, stdout_data.decode())
    if stderr_data:
        append_to_view(v, stderr_data.decode())
    sublime.active_window().run_command("show_panel", args={"panel":"output.Perforce"})

    # if p.returncode != 0:
    #     sublime.message_dialog(stderr_data.decode())

def run_command(command, dirname):
    sublime.active_window().show_input_panel(
        "Perforce Password",
        "",
        lambda passwd: post_password(passwd, command, dirname),
        None, None
    )


class PerforceAdd(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = self.view.file_name()
        dirname = os.path.dirname(filename)
        run_command(["add", filename], dirname)

class PerforceEdit(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = self.view.file_name()
        dirname = os.path.dirname(filename)
        run_command(["edit", filename], dirname)

class PerforceDiff(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = self.view.file_name()
        dirname = os.path.dirname(filename)
        run_command(["diff", filename], dirname)

class PerforceReconcile(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = self.view.file_name()
        dirname = os.path.dirname(filename)
        run_command(["reconcile", filename], dirname)

class PerforceRevert(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = self.view.file_name()
        dirname = os.path.dirname(filename)
        run_command(["revert", filename], dirname)

class PerforceStatus(sublime_plugin.TextCommand):
    def run(self, edit):
        dirname = os.getcwd()
        run_command(["status"], dirname)

class PerforceHelp(sublime_plugin.TextCommand):
    def run(self, edit):
        dirname = os.getcwd()
        run_command(["help"], dirname)

