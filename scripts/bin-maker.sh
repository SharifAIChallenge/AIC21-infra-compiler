# in all the functions bel
# check weather or not exitcode was 0 and return
function check {
    if [ $1 -eq 0 ];then
        info "code compiled successfully!"
    else
        fatal "couldn't compile code!"
        exit -1
    fi
}

# compiles the python client into binary file
# the precedure taken here are based on the code
# structure described in the github repo lined below
# https://github.com/SharifAIChallenge/AIC21-client-python
# the binary compiler used here is pyinstaller pakage should
# be installed in the running enviorment (docker, virtualenv, ...)
function python-bin {
    info "language detected: python"
    info "start compiling using pyinstaller"
    pyinstaller --onefile Controller.py >>$LOG_PATH 2>&1 
    check $?
    mv dist/Controller $BIN_PATH
}    

# compiles the cpp client into binary file
# the precedure taken here are based on the code
# structure described in the github repo lined below
# https://github.com/SharifAIChallenge/AIC21-client-cpp
# the binary compiler used here is cmake mixed with "make"
# thus both packages should be installed in the running 
# enviorment (docker, virtualenv, ...)
function cpp-bin {

    info "language detected: C"
    info "start compiling using CMAKE"
    mkdir build
    cd build
    cmake .. >>$LOG_PATH 2>&1
    make >>$LOG_PATH 2>&1
    check $?
    mv client/client $BIN_PATH
    cd ..    
}

# not yet supported
# if you are next gen "team e Zrsakht" then "dastet ro mibuse" 
function java-bin {
    fatal "not currently supported!\n use [jar] instead"
    exit -1
}

# the function below turns the jar file into linux executalbe file
# and its not yet optimized (turning jar into binary)
# holds up with the API just lacks performance
# again:
# if you are next gen "team e Zrsakht" then "dastet ro mibuse" 
function jar-bin {

    info "language detected: jar"
    info "start compiling using jar-stub"
    cat ../jar-stub.sh `ls | grep "jar" | head -n1` >$BIN_PATH 2>>$LOG_PATH  
    check $?
}

# pun intended
function bin-bin {
    warn "no compiling needed!"
    mv `ls | head -n1` $BIN_PATH 
}