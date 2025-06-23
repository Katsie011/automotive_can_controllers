setup_bookworm() {
    # Download the library
    wget https://github.com/joan2937/lg/archive/master.zip
    if [ $? -ne 0 ]; then
        echo "Error: Failed to download lg master.zip from GitHub."
        exit 1
    fi

    # Unzip the archive
    unzip master.zip
    if [ $? -ne 0 ]; then
        echo "Error: Failed to unzip master.zip."
        exit 1
    fi

    # Change directory
    cd lg-master
    if [ $? -ne 0 ]; then
        echo "Error: Failed to change directory to lg-master."
        exit 1
    fi

    # Install the library
    sudo make install
    if [ $? -ne 0 ]; then
        echo "Error: Failed to run 'sudo make install' in lg-master."
        exit 1
    fi

    # For more information, please refer to the official website: https://github.com/gpiozero/lg
}

setup_bullseye() {
    # Download the library
    wget https://github.com/joan2937/lg/archive/master.zip
    if [ $? -ne 0 ]; then
        echo "Error: Failed to download lg master.zip from GitHub."
        exit 1
    fi

    # Unzip the archive
    unzip master.zip
    if [ $? -ne 0 ]; then
        echo "Error: Failed to unzip master.zip."
        exit 1
    fi

    # Change directory
    cd lg-master
    if [ $? -ne 0 ]; then
        echo "Error: Failed to change directory to lg-master."
        exit 1
    fi

    # Install the library
    sudo make install
    if [ $? -ne 0 ]; then
        echo "Error: Failed to run 'sudo make install' in lg-master."
        exit 1
    fi

    # For more information, please refer to the official website: https://github.com/gpiozero/lg
}

setup_python(){
    sudo apt-get update
    if [ $? -ne 0 ]; then
        echo "Error: Failed to update package list (apt-get update)."
        exit 1
    fi

    sudo apt-get install -y python3-serial
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install python3-serial."
        exit 1
    fi

    sudo apt-get install -y python3-can
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install python3-can."
        exit 1
    fi
}

# Detect the Linux distribution (Bookworm or Bullseye)
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [[ "$VERSION_CODENAME" == "bookworm" ]]; then
        setup_bookworm
        if [ $? -ne 0 ]; then
            echo "Error: setup_bookworm failed."
            exit 1
        fi
    elif [[ "$VERSION_CODENAME" == "bullseye" ]]; then
        setup_bullseye
        if [ $? -ne 0 ]; then
            echo "Error: setup_bullseye failed."
            exit 1
        fi
    else
        echo "Error: Unsupported Linux distribution. Only Bookworm or Bullseye are supported."
        exit 1
    fi

    echo "Setting up python libraries"
    setup_python
    if [ $? -ne 0 ]; then
        echo "Error: setup_python failed."
        exit 1
    fi
else
    echo "Error: Cannot determine Linux distribution (missing /etc/os-release)."
    exit 1
fi
