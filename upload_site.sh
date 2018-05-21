#!/bin/sh

find . -name .DS_Store -delete
ssh uppsala rm -rf public_html/gspd/
scp -r UI/ uppsala:public_html/gspd
