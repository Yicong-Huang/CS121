'''
Created on Oct 20, 2016
@author: Rohan Achar
'''
from rtypes.pcc.attributes import dimension, primarykey, predicate
from rtypes.pcc.types.subset import subset
from rtypes.pcc.types.set import pcc_set
from rtypes.pcc.types.projection import projection
from rtypes.pcc.types.impure import impure
from datamodel.search.server_datamodel import Link, ServerCopy

@pcc_set
class Yicongh1ZicanlHwoLink(Link):
    USERAGENTSTRING = "Yicongh1ZicanlHwo"

    @dimension(str)
    def user_agent_string(self):
        return self.USERAGENTSTRING

    @user_agent_string.setter
    def user_agent_string(self, v):
        # TODO (rachar): Make it such that some dimensions do not need setters.
        pass


@subset(Yicongh1ZicanlHwoLink)
class Yicongh1ZicanlHwoUnprocessedLink(object):
    @predicate(Yicongh1ZicanlHwoLink.download_complete, Yicongh1ZicanlHwoLink.error_reason)
    def __predicate__(download_complete, error_reason):
        return not (download_complete or error_reason)


@impure
@subset(Yicongh1ZicanlHwoUnprocessedLink)
class OneYicongh1ZicanlHwoUnProcessedLink(Yicongh1ZicanlHwoLink):
    __limit__ = 1

    @predicate(Yicongh1ZicanlHwoLink.download_complete, Yicongh1ZicanlHwoLink.error_reason)
    def __predicate__(download_complete, error_reason):
        return not (download_complete or error_reason)

@projection(Yicongh1ZicanlHwoLink, Yicongh1ZicanlHwoLink.url, Yicongh1ZicanlHwoLink.download_complete)
class Yicongh1ZicanlHwoProjectionLink(object):
    pass
