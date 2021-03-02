from gather import glacier_factory, satellite_download

gf = glacier_factory.GlacierFactory("wgi_feb2012.csv")

downloader = satellite_download.Download(gf)
downloader.download_glaciers()
