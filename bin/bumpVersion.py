#!/usr/bin/python3
import sys
import re


def usage():
    print('Usage: bumpVersion -v NEWVERSION')
    print('       bumpVersion [major|minor|patch|dev}')
    sys.exit(1)


versionRE = '^version\\s*=\\s\"(.*)\"\\s*'
fileName = 'src/pystream/__about__.py'


def get_current_version():
    version = ''
    with open(fileName) as f:
        for line in f:
            match = re.match(versionRE, line)
            if match:
                print(line)
                version = match.group(1)
                break
    s_array = version.split('.')
    print(s_array)
    i_array = list(map(lambda s: int(s), s_array))
    if len(i_array) == 4:
        return i_array
    return i_array + [0]


def fmt_version(vers):
    v = "{0}.{1}.{2}".format(vers[0], vers[1], vers[2])
    if vers[3] == 0:
        return v
    return v + ".{0}".format(vers[3])


def bump_major(vers):
    return [vers[0] + 1, 0, 0, 0]


def bump_minor(vers):
    return [vers[0], vers[1] + 1, 0, 0]


def bump_patch(vers):
    return [vers[0], vers[1], vers[2] + 1, 0]


def bump_dev(vers):
    return [vers[0], vers[1], vers[2], vers[3] + 1]


bumpFuncs = {
    'major': bump_major,
    'minor': bump_minor,
    'patch': bump_patch,
    'dev': bump_dev}


def parse_args():
    if len(sys.argv) < 2:
        usage()
    if sys.argv[1] == '-v':
        if len(sys.argv) < 3:
            usage()
        return sys.argv[2]
    if not sys.argv[1] in bumpFuncs:
        usage()
    current_version = get_current_version()
    return fmt_version(bumpFuncs[sys.argv[1]](current_version))


def update_version(new_version):
    out_lines = []
    with open(fileName) as f:
        for line in f:
            match = re.match(versionRE, line)
            if match:
                out_lines.append('version = "{0}"\n'.format(new_version))
                continue
            out_lines.append(line)
    with open(fileName, 'w') as fw:
        fw.writelines(out_lines)


if __name__ == '__main__':
    newVersion = parse_args()
    print("Setting version to " + newVersion)
    update_version(newVersion)
