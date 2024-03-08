class Plate:
    _pid: int = None
    _pnum: str = None
    _remark: str = None

    def __init__(self, pid, pnum, remark):
        self._pid = pid
        self._pnum = pnum
        self._remark = remark

    @property
    def pnum(self):
        return self._pnum

    @pnum.setter
    def pnum(self, pnum):
        self._pnum = pnum

    @property
    def remark(self):
        return self._remark

    @remark.setter
    def remark(self, remark):
        self._remark = remark
