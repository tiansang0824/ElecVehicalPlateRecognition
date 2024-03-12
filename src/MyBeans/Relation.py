class Relation:
    _rid = None
    _uid = None
    _pid = None
    _remark = None

    def __init__(self, rid, uid, pid, remark=None):
        self._rid = rid
        self._uid = uid
        self._pid = pid
        self._remark = remark

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, pid):
        self._pid = pid

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        self.uid = uid

    @property
    def rid(self):
        return self._rid

    @rid.setter
    def rid(self, rid):
        self._rid = rid

    @property
    def remark(self):
        return self._remark

    @remark.setter
    def remark(self, remark):
        self._remark = remark
