# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 11:22:45 2021

@author: michele
"""

import sys
import org.apache.hadoop.fs.{FileSystem,Path}

val fs = FileSystem.get(spark.sparkContext.hadoopConfiguration)
new PrintWriter(fs.create(new Path(sys.argv[1]))){
    write("col1,col2,col3\n")
  }