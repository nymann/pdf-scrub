COMPONENT?=pdf_scrub
VERSION:=src/${COMPONENT}/version.py
.DEFAULT:help
include make/help.mk
include make/common.mk
include make/install.mk
include make/test.mk
include make/lint.mk
include make/ci.mk

