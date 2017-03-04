
# url_post_map = {
#     '/config' : config_post
# }

# url_get_map = {
#     '/' : root_get,
#     '/version' : version_get,
#     '/config' : config_get
# }

######################
# URL GET
######################
def root_get(fisher, serverhandle):
    """root_get
    """
    print "root_get"
    fisher.root_get(serverhandle)
    

def version_get(fisher, serverhandle):
    """version_get
    """
    fisher.version_get(serverhandle)

def topo_get(fisher, serverhandle):
    """version_get
    """
    fisher.topo_get(serverhandle)

######################
# URL POST
######################
def config_post(fisher, serverhandle):
    """config_post
    """
    fisher.config_post(serverhandle)
