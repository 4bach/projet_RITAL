#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import Document
import Parser 

if __name__=="__main__":
    d = Document(Parser("data/cacm/cacm.txt").buildDocCollectionSimple())
    
