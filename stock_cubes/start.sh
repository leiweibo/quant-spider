#! /bin/bash
function setupChromeDriver() {
    echo "start to check chrome driver ..."
    chromedriver -v
    if [ $? -eq 0 ]; then
        echo "chromedriver is install"
    else
        chromeDownloadUrl = ""
        sysos = ""

        echo "chrome driver not install yet."
        if [ "$(uname)"=="Linux" ]; then
            sysos="linux"
            echo "You are using linux."
        elif [ "$(uname)"=="Darwin" ]; then 
            sysos="mac"
            echo "Your are using MacOS."
        fi

        echo $sysos
        echo "plese check your local chrome version, and chose the correspond chrome driver version"
        echo "please refer here: https://sites.google.com/a/chromium.org/chromedriver/downloads"
        chromeDownloadUrl="http://chromedriver.storage.googleapis.com/75.0.3770.140/chromedriver_${sysos}64.zip"
        echo "The final down url is: " $chromeDownloadUrl
        zipFileName="chromedriver_${sysos}64.zip"
        echo "The zip file is: ${zipFileName}"
        
        if [ -n "$chromeDownloadUrl" ]; then
            if [ -f "$zipFileName" ]; then 
                echo "zip" exists, remove it.
                rm "$zipFileName"
        
            echo "Start to down from url:" $chromeDownloadUrl
            wget -N $chromeDownloadUrl
            fi
        else
            echo "chrome down load url is empty."
            exit 1
        fi
        
        # unzip -v
        
        # if [ $? -ne 0 ]; then
        #     echo "unzipnot installed."
        #     sudo apt install unzip
        # fi
        
        if [ -f "chromedriver" ]; then
            echo "chromedriver file exists, remove it."
            rm "chromedriver"
        fi
        unzip $zipFileName
        chmod 777 chromedriver
        ls -lr chromedriver
    fi
}

function main() {
    setupChromeDriver
}

main