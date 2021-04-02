from process.crawlers.crawler import Crawler
from process.entities.scene import Scene

import os


class SceneCrawler(Crawler):
    def __init__(self, root):
        Crawler.__init__(self, root)
