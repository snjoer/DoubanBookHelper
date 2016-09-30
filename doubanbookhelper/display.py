import subprocess

def display(filepath):
    subprocess.call(['open', '-a', 'TextEdit', filepath])
