from django_rq import job 
from rq import get_current_job
from kate.engine.calc import calc_move, SearchComm
from kate.modules import interface


@job("high")
def job_calc_and_do_move(modelmatch, match):
    job = get_current_job()
    job.meta['matchid'] = match.id
    searchcomm = SearchComm()
    job.meta['searchcomm'] = searchcomm
    job.save_meta()

    candidates = calc_move(match, searchcomm)
    gmove = candidates[0]
    interface.do_move(modelmatch, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
