def get_port_number_from_first_arg(argv):
    if len(argv) > 0 and not argv[0].startswith('-'):
        return argv[0]
    else:
        return None
