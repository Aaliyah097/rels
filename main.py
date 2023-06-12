import sys


__doc__ = "enter point"



if __name__ == '__main__':
    if 'prod' in sys.argv[1:]:
        app.app.run(host='0.0.0.0')
    else:
        app.app.run()
