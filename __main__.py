from gather import glacier_factory, satellite_download

downloader = satellite_download.Download("wgi_feb2012.csv")
downloader.download_glaciers()
