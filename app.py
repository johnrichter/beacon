from pprint import pprint
import beacon


if __name__ == '__main__':
    args = beacon.parse_arguments()
    pprint('--- args ---\n', args)
