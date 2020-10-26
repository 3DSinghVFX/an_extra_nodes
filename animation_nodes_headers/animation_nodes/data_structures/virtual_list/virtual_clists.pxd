from . virtual_list cimport VirtualList

from .. lists.base_lists cimport Vector3DList

from ... math.vector cimport Vector3

cdef class VirtualVector3DList(VirtualList):
    # Should only be called with a positiv index
    cdef Vector3 * get(self, Py_ssize_t i)


from .. lists.base_lists cimport Vector2DList

from ... math.vector cimport Vector2

cdef class VirtualVector2DList(VirtualList):
    # Should only be called with a positiv index
    cdef Vector2 * get(self, Py_ssize_t i)


from .. lists.base_lists cimport Matrix4x4List

from ... math.matrix cimport Matrix4

cdef class VirtualMatrix4x4List(VirtualList):
    # Should only be called with a positiv index
    cdef Matrix4 * get(self, Py_ssize_t i)


from .. lists.base_lists cimport EulerList

from ... math.euler cimport Euler3

cdef class VirtualEulerList(VirtualList):
    # Should only be called with a positiv index
    cdef Euler3 * get(self, Py_ssize_t i)


from .. lists.base_lists cimport QuaternionList

from ... math.quaternion cimport Quaternion

cdef class VirtualQuaternionList(VirtualList):
    # Should only be called with a positiv index
    cdef Quaternion * get(self, Py_ssize_t i)


from .. lists.base_lists cimport ColorList

from ... math.color cimport Color

cdef class VirtualColorList(VirtualList):
    # Should only be called with a positiv index
    cdef Color * get(self, Py_ssize_t i)


from .. lists.base_lists cimport FloatList



cdef class VirtualFloatList(VirtualList):
    # Should only be called with a positiv index
    cdef float  get(self, Py_ssize_t i)


from .. lists.base_lists cimport DoubleList



cdef class VirtualDoubleList(VirtualList):
    # Should only be called with a positiv index
    cdef double  get(self, Py_ssize_t i)


from .. lists.base_lists cimport LongList



cdef class VirtualLongList(VirtualList):
    # Should only be called with a positiv index
    cdef long  get(self, Py_ssize_t i)


from .. lists.base_lists cimport BooleanList



cdef class VirtualBooleanList(VirtualList):
    # Should only be called with a positiv index
    cdef char  get(self, Py_ssize_t i)
