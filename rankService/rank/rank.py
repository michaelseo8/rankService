class Rank(object):
    def __init__(self, rank, url, imageurl, mallname, title, productid):
        self.rank = rank
        self.url = url
        self.imageurl = imageurl
        self.mallname = mallname
        self.title = title
        self.productid = productid
        self.latestRank = None
        self.latestSearchDate = None

