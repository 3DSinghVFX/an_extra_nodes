cdef struct Vector2:
    float x, y

cdef struct Vector3:
    float x, y, z

cdef struct Vector4:
    float x, y, z, w

cdef char isExactlyZeroVec3(Vector3* v)
cdef char almostZeroVec3(Vector3* v)
cdef char isCloseVec3(Vector3* a, Vector3* b)

cdef float lengthVec3(Vector3* v)
cdef float lengthSquaredVec3(Vector3* v)

cdef void scaleVec3(Vector3* target, Vector3* a, float factor)
cdef void scaleVec3_Inplace(Vector3* v, float factor)

cdef void addVec3(Vector3* target, Vector3* a, Vector3* b)
cdef void addVec3_Inplace(Vector3* target, Vector3* other)
cdef void subVec3(Vector3* target, Vector3* a, Vector3* b)
cdef void multVec3(Vector3* target, Vector3* a, Vector3* b)
cdef void divideVec3(Vector3* target, Vector3* a, Vector3* b)

cdef float dotVec3(Vector3* a, Vector3* b)
cdef float angleVec3(Vector3 *a, Vector3 *b)
cdef void crossVec3(Vector3* result, Vector3* a, Vector3* b)
cdef float scalarTripleProduct(Vector3 *a, Vector3 *b, Vector3 *c)
cdef float angleNormalizedVec3(Vector3 *a, Vector3 *b)

cdef void projectVec3(Vector3* result, Vector3* a, Vector3* b)
cdef void reflectVec3(Vector3* result, Vector3* v, Vector3* axis)
cdef void projectOnCenterPlaneVec3(Vector3 *result, Vector3 *v, Vector3 *planeNormal)

cdef void normalizeVec3_InPlace(Vector3* v)
cdef void normalizeVec3(Vector3* target, Vector3* v)
cdef void normalizeLengthVec3_Inplace(Vector3* v, float length)
cdef void normalizeLengthVec3(Vector3* target, Vector3* v, float length)

cdef float distanceVec3(Vector3* a, Vector3* b)
cdef float distanceSquaredVec3(Vector3* a, Vector3* b)

cdef void absoluteVec3(Vector3* target, Vector3* source)
cdef void snapVec3(Vector3* target, Vector3* v, Vector3* step)
cdef void mixVec3(Vector3* target, Vector3* a, Vector3* b, float factor)

cdef void rotateAroundAxisVec3(Vector3 *target, Vector3 *v, Vector3 *axis, float angle)
