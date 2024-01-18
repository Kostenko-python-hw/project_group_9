SHUTDOWN_COMMANDS = ('good bye', 'close', 'exit')


class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


note_header = "|{:^6}|{:^52}|{:^42}|{:^82}|".format(
    'id', 'title', 'tags', 'description')
underline = '_' * 187
