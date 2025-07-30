import os


def main():
    try:
        u_pythonpath = os.environ['PYTHONPATH']
        print(f"pythonpath -> {u_pythonpath}")
    except KeyError:
        print(f"KeyError PYTHONPATH")
        exit(1)


if __name__ == '__main__':
    main()