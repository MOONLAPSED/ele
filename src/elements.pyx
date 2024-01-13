# cython: language_level=3

cdef extern from "stdio.h":
    int printf(const char *format, ...)

cdef extern from "Python.h":
    char* PyString_AsString(object string)

cdef class Frame:
    cdef unsigned char header
    cdef bytes payload

    def __cinit__(self, unsigned char header, bytes payload):
        # Corrected assignment without using self.
        header = header
        payload = payload
        printf("Frame initialized with header %d and payload %s\n", header, payload)
