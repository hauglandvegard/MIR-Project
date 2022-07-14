import sys
import colorama


# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#background-colors
def esc(code):
    pass


# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=20, fill='█', print_end="\r",
                       color=colorama.Fore.YELLOW, header='', footer=''):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    if iteration == 0 and header:
        print(header)

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length - 1)

    print(color + f'\r{prefix} |{bar}| {percent}% {suffix} ({iteration}/{total})', end=print_end)

    if iteration == total:
        print(colorama.Fore.GREEN + f'{prefix} |{bar}| {percent}% {suffix}')
        print(colorama.Fore.RESET + footer + '\n')

    sys.stdout.flush()
