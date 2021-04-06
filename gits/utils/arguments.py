import argparse

# from gather import satellite_download
from preprocess.crawlers.glacier_crawler import GlacierCrawler


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
        self.add_process_args()

    def add_download_args(self) -> None:
        download_parser = self.subparsers.add_parser('download',
                                                     add_help=True)

        download_parser.add_argument('--csv',
                                     help='Path to the csv file.',
                                     default=self.DEFAULT_CSV_PATH,
                                     type=str,
                                     dest='csv')

        download_parser.add_argument('-c',
                                     '--cloud-cover',
                                     help='Maximum cloud coverage allowed for a scene.',
                                     default=self.DEFAULT_J,
                                     type=int,
                                     dest='c')

        download_parser.add_argument('-d',
                                     '--download-directory',
                                     help='Path to the output folder which will contain the data set results.',
                                     type=str,
                                     dest='d')

        download_parser.add_argument('-j',
                                     '--jobs',
                                     help='Number of threads which will search and download.',
                                     default=self.DEFAULT_J,
                                     type=int,
                                     dest='j')

        download_parser.set_defaults(func=set_download_callback)

    def add_process_args(self) -> None:
        process_parser = self.subparsers.add_parser('process',
                                                    add_help=True)
        process_parser.add_argument('--input',
                                    help='Path to the input folder which contains the dataset of'
                                         'glaciers.',
                                    type=str,
                                    dest='input')
        process_parser.set_defaults(func=set_process_callback)


def activate_arguments() -> None:
    arguments = CMDArgs()
    args = arguments.parser.parse_args()

    args.func(args)


def set_download_callback(args) -> None:
    """
    The default function for download sub parser.
    :param args: Arguments passed through command line for download.
    """
    # downloader = satellite_download.Download(args.csv, args.c, args.d, args.j)
    # downloader.download_glaciers()


def set_process_callback(args) -> None:
    crawler = GlacierCrawler(args.input)
    crawler.crawl()
