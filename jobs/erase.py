from .scons import main as scons


help_title="清除芯片内部Flash"

def main(argv):
    exclusive_kill()
