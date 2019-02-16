#include <Python.h>
#include <stdio.h>
#include <string.h>

static PyObject* permission(PyObject* self, PyObject* args)
{
	FILE* fp=fopen("/sys/block/mmcblk0/device/serial","r");

	char *temp;
	char serial[11];
	char serial_this[11] = "0x3b5781b3";

	temp=fgets(serial, 11, fp);

	fclose(fp);

	if (strcmp(serial,serial_this) == 0) {
		return Py_BuildValue("iiiiii",24,13,800000,5,255,1);
	}

	else {
		return Py_BuildValue("iiiiii",0,0,0,0,0,0);
	}
}

static PyMethodDef Methods[] =
{
	{"get", permission, METH_VARARGS},
	{NULL, NULL, 0}
};

PyMODINIT_FUNC initperm(void)
{
	(void) Py_InitModule("perm", Methods);
}
