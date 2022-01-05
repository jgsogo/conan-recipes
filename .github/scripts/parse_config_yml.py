import yaml

def work(filename):
    with open(filename, "r") as stream:
        data = yaml.safe_load(stream)

        for v, info in data["versions"].items():
            print(f"{info['folder']} {v}")

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    work(filename)

