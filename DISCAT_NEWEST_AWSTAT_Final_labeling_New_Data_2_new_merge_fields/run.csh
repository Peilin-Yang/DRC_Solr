#!/bin/tcsh 

#set path enviroment variable
setenv PATH /local/headnode2/yzhan/java/jdk1.8.0_20/bin:/local/headnode2/yzhan/java/jre1.8.0_20/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin
#set CLASSPATH
setenv CLASSPATH /local/headnode2/yzhan/java/jdk1.8.0_20/lib:/local/headnode2/yzhan/java/jre1.8.0_20/lib
# JAVA_HOME (JDK path)
setenv JAVA_HOME /local/headnode2/yzhan/java/jdk1.8.0_20


cd /local/headnode2/yzhan/solr/DISCAT


nohup java -Dsolr -Djetty.port=10000 -jar start.jar &


