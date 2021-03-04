import argparse

from gather import satellite_download

class CMDArgs:
    """
    Class which handles argument parsing for the command line interface.
    """
    DEFAULT_J = 10
    DEFAULT_CSV_PATH = "wgi_feb2012.csv"

    def __init__(self):
        self.parser = argparse.ArgumentParser(add_help=True)
        self.subparsers = self.parser.add_subparsers()

        self.add_download_args()

    def add_download_args(self):
        download_parser = self.subparsers.add_parser('download',
                                                     add_help=True)
        
        download_parser.add_argument('--csv',
                                     help='Path to the csv file.',
                                     default=self.DEFAULT_CSV_PATH,
                                     type=str,
                                     dest='csv')

        download_parser.add_argument('--ddir',
                                     help='Path to the output folder which will contain the data set results.',
                                     type=str,
                                     dest='ddir')

        download_parser.add_argument('-j',
                                     help='Number of threads which will search and download.',
                                     default=self.DEFAULT_J,
                                     type=int,
                                     dest='j')

        download_parser.set_defaults(func=set_download_callback)


def activate_arguments() -> None:
    arguments = CMDArgs()
    args = arguments.parser.parse_args()

    args.func(args)


def set_download_callback(args) -> None:
    """
    The default function for download sub parser.
    :param args: Arguments passed through command line for download.
    """
    downloader = satellite_download.Download(args.csv, args.ddir, args.j)
    downloader.download_glaciers()
