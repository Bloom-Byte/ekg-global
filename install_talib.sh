#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if the OS is Linux-based
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
  echo "This script is intended for Linux-based systems only."
  exit 1
fi

# Default values
TA_LIB_VERSION="0.4.0"
TA_LIB_URL="http://prdownloads.sourceforge.net/ta-lib/ta-lib-${TA_LIB_VERSION}-src.tar.gz"
PYTHON_VERSION=$(python3 --version | awk '{print $2}' | cut -d'.' -f1,2)  # Default to active Python version

# Usage function
usage() {
  echo "Usage: $0 [-v version] [-u url] [-p python_version]"
  echo "  -v version         Specify the version of TA-Lib source code to install (default: ${TA_LIB_VERSION})"
  echo "  -u url             Specify the URL to the TA-Lib source code (default: ${TA_LIB_URL})"
  echo "  -p python_version  Specify the Python version for the development headers (default: ${PYTHON_VERSION})"
  exit 1
}

# Parse command-line options
while getopts ":v:u:p:" opt; do
  case ${opt} in
    v )
      TA_LIB_VERSION=$OPTARG
      TA_LIB_URL="http://prdownloads.sourceforge.net/ta-lib/ta-lib-${TA_LIB_VERSION}-src.tar.gz"
      ;;
    u )
      TA_LIB_URL=$OPTARG
      ;;
    p )
      PYTHON_VERSION=$OPTARG
      ;;
    \? )
      echo "Invalid option: -$OPTARG" >&2
      usage
      ;;
    : )
      echo "Option -$OPTARG requires an argument." >&2
      usage
      ;;
  esac
done

# Update and install build tools
echo "Updating package list and installing build tools..."
sudo apt update
sudo apt install build-essential wget -y

# Install Python development headers for the specified or active Python version
echo "Installing Python ${PYTHON_VERSION} development headers..."
sudo apt-get install "python${PYTHON_VERSION}-dev" -y || { echo "Failed to install Python ${PYTHON_VERSION} development headers"; exit 1; }

# Create directory for TA-Lib version and navigate to it
mkdir -p "ta-lib-${TA_LIB_VERSION}"
cd "ta-lib-${TA_LIB_VERSION}"

# Download and extract the TA-Lib source code into the version-specific directory
echo "Downloading TA-Lib source code from ${TA_LIB_URL}..."
wget "$TA_LIB_URL" -O "ta-lib-${TA_LIB_VERSION}-src.tar.gz" || { echo "Failed to download TA-Lib source code"; exit 1; }
echo "Extracting TA-Lib source code..."
tar --strip-components=1 -xzf "ta-lib-${TA_LIB_VERSION}-src.tar.gz" || { echo "Failed to extract TA-Lib source code"; exit 1; }

# Configure and build TA-Lib
echo "Configuring and building TA-Lib..."
./configure --prefix=/usr || { echo "Configuration failed"; exit 1; }
make || { echo "Build failed"; exit 1; }

# Install TA-Lib
echo "Installing TA-Lib..."
sudo make install || { echo "Installation failed"; exit 1; }

# Install TA-Lib Python wrapper
echo "Installing TA-Lib Python wrapper..."
pip install ta-lib || { echo "Failed to install TA-Lib Python wrapper"; exit 1; }

# Test the installation by importing talib in Python
echo "Testing TA-Lib installation..."
if python3 -c "import talib"; then
  echo "TA-Lib installed successfully"
else
  echo "ImportError detected. Exporting LD_LIBRARY_PATH or adding to ld.so.conf..."
  
  # Option 1: Export LD_LIBRARY_PATH (temporary for the session)
  export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
  
  # Option 2: Add /usr/local/lib to /etc/ld.so.conf and run ldconfig (permanent)
  echo "/usr/local/lib" | sudo tee -a /etc/ld.so.conf
  sudo /sbin/ldconfig
fi

echo "TA-Lib installation complete."
