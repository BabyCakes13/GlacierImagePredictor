from gather import glacier_factory

gf = glacier_factory.GlacierFactory("wgi_feb2012.csv")
glacier = gf.get_next_glacier()
print(glacier)
