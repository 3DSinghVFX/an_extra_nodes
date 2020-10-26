from . action_base cimport *
from .. lists.base_lists cimport FloatList, IntegerList

ctypedef void (*EvaluateFunction)(void *self, float frame, Py_ssize_t index, float *target)


cdef class BoundedAction(Action):
    cdef BoundedActionEvaluator getEvaluator_Limited(self, list channels)
    cpdef BoundedActionEvaluator getEvaluator_Full(self, list channels, FloatList defaults)

cdef class BoundedActionEvaluator(ActionEvaluator):
    pass
    cdef void evaluateBounded(self, float t, Py_ssize_t index, float *target)

    cpdef float getStart(self, Py_ssize_t index)
    cpdef float getEnd(self, Py_ssize_t index)
    cpdef float getLength(self, Py_ssize_t index)

cdef class SimpleBoundedAction(BoundedAction):
    cdef list getEvaluateFunctions(self)
    cdef newFunction(self, void *function, list channels)

    cdef float getStart(self, Py_ssize_t index)
    cdef float getEnd(self, Py_ssize_t index)
    cdef float getLength(self, Py_ssize_t index)

cdef class UnboundedAction(Action):
    cdef UnboundedActionEvaluator getEvaluator_Limited(self, list channels)
    cpdef UnboundedActionEvaluator getEvaluator_Full(self, list channels, FloatList defaults)

cdef class UnboundedActionEvaluator(ActionEvaluator):
    pass

cdef class SimpleUnboundedAction(UnboundedAction):
    cdef list getEvaluateFunctions(self)
    cdef newFunction(self, void *function, list channels)
