from django_rq import job 
from rq import get_current_job
from kate.engine.calc import calc_move
from kate.modules import interface




@job("high")
def job_calc_and_do_move(modelmatch, match):
    job = get_current_job()
    job.meta[interface.Msgs.META_MATCHID] = match.id
    job.meta[interface.Msgs.META_ISALIVE] = True
    job.meta[interface.Msgs.META_TERMINATE] = False
    job.meta[interface.Msgs.META_CURRENTSEARCH] = None
    job.save_meta()
    msgs = interface.Msgs(job)

    candidates = calc_move(match, msgs)
    if(job.meta[interface.Msgs.META_ISALIVE] == True):
        gmove = candidates[0]
        interface.do_move(modelmatch, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

