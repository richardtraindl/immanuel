from django_rq import job 
from rq import get_current_job
from kate.engine.calc import calc_move, SearchComm
from kate.modules import interface


@job("high")
def job_calc_and_do_move(modelmatch, match):
    job = get_current_job()
    job.meta['matchid'] = match.id
    job.meta['currentsearch'] = ""
    job.meta['terminate'] = 0
    job.save_meta()

    searchcomm = SearchComm()
    fetchcandidates = interface.FetchCandidatesThread(match.id, searchcomm)
    fetchcandidates.start()
    candidates = calc_move(match, searchcomm)
    fetchcandidates.join(3.0)
    gmove = candidates[0]
    interface.do_move(modelmatch, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

