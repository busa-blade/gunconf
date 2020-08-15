import argparse
from gunconf.ui.gunapp import GunApp
from gunconf.controller import Controller


def parseArgs():
    """ parse arguments """
    parser = argparse.ArgumentParser(description='gun configuration utility')
    parser.add_argument('--width', type=int, help='screen width')
    parser.add_argument('--height', type=int, help='screen height')
    return parser.parse_args()



if __name__ == '__main__':

    # parse arg
    args = parseArgs()

    # allocate controler
    controller = Controller()

    # allocate app
    app = GunApp(args.width, args.height)
    app.setCtrl(controller)

    controller.setCb(app.ctrlCb)
    controller.run()

    app.run()
