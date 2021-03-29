#! /bin/bash

LANG=$1
ROOT_DIR=$PWD
LOG_PATH=$ROOT_DIR/compile.log
BIN_PATH=$ROOT_DIR/binary

# takes a string and append it to the log file as well as the console tty
function log {
  echo "$1" | tee -a $LOG_PATH
}

# generates info log
function info {
    log "===[INFO]===[`date +'%F-%T'`]=== : $1"
}
# generates warn log
function warn {
    log "===[WARN]===[`date +'%F-%T'`]=== : $1"
}
# generates FATAL log and exits with -1
function fatal {
    log "===[FATAL]==[`date +'%F-%T'`]=== : $1"
    # clean up
    rm -rf /home/isolated
    exit -1
}
# check weather or not exitcode was 0 and return
function check {
    if [ $1 -eq 0 ];then
        info "code compiled successfully!"
    else
        fatal "couldn't compile code!"
    fi
}
    
 
# empty log file
echo "" > $LOG_PATH

# make an isolated aread
mkdir /home/isolated
cp -r * /home/isolated
cd /home/isolated
info "made an isolated area"

info "entered the code base"

#compile
case $LANG in

  python|py|python3|py3|PYTHON|PY|PYTHON3|PY3)
    
    info "language detected: python"
    info "start compiling using pyinstaller"
    pyinstaller --onefile Controller.py >$LOG_PATH 2>&1
    check $?
    mv dist/Controller $BIN_PATH
    
    ;;

  cpp|c|C|CPP)
    info "language detected: C"
    info "start compiling using CMAKE"
    mkdir build
    cd build
    cmake .. >$LOG_PATH 2>&1
    make >$LOG_PATH 2>&1
    check $?
    mv client/client $BIN_PATH
    
    ;;

  java|JAVA)
    fatal "not currently supported!\n use [jar] instead"
    
    ;;

  jar|JAR)
    info "language detected: jar"
    info "start compiling using jar-stub"
    
    cat /home/.jar-stub `ls | head -n1` > $BIN_PATH 2> $LOG_PATH  
    check $?
    
    ;;

  bin|BIN)
    warn "no compiling needed!"
    mv `ls | head -n1` $BIN_PATH 
    ;;

  *)
    fatal "type unknown!"
    ;;
esac

chmod +x $BIN_PATH
# clean up
rm -rf /home/isolated

