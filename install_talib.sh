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
VENV_DIR="ta-lib-test-env"  # Default test virtual environment directory
VENV_CREATED=false  # Flag to track if the virtual environment was created

# Usage function
usage() {
  echo "Usage: $0 [-v version] [-u url] [-p python_version] [-e venv_dir]"
  echo "  -v version         Specify the version of TA-Lib source code to install (default: ${TA_LIB_VERSION})"
  echo "  -u url             Specify the URL to the TA-Lib source code (default: ${TA_LIB_URL})"
  echo "  -p python_version  Specify the Python version for the development headers (default: ${PYTHON_VERSION})"
  echo "  -e venv_dir        Specify the virtual environment directory (default: ${VENV_DIR})"
  exit 1
}

# Parse command-line options
while getopts ":v:u:p:e:" opt; do
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
    e )
      VENV_DIR=$OPTARG
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

# Install global TA-Lib C library
echo "Installing global TA-Lib C library..."

# Update and install build tools
apt update
apt install build-essential wget -y

# Check if the required Python version is available
if ! apt list --installed | grep -q "python${PYTHON_VERSION}-dev"; then
  echo "Python ${PYTHON_VERSION} development headers not found. Adding deadsnakes PPA to install it..."
  
  # Add deadsnakes PPA and install python3.10-dev (or whichever version is required)
  apt install software-properties-common -y
  add-apt-repository ppa:deadsnakes/ppa -y
  apt update
  apt install "python${PYTHON_VERSION}-dev" -y || { echo "Failed to install Python ${PYTHON_VERSION} development headers"; exit 1; }
else
  echo "Python ${PYTHON_VERSION}-dev is already installed."
fi

# Create directory for TA-Lib version and navigate to it
mkdir -p "ta-lib-${TA_LIB_VERSION}"
cd "ta-lib-${TA_LIB_VERSION}"

echo "Downloading TA-Lib source code..."
wget "$TA_LIB_URL" -O "ta-lib-${TA_LIB_VERSION}-src.tar.gz" || { echo "Failed to download TA-Lib source code"; exit 1; }
echo "Extracting TA-Lib source code..."
tar --strip-components=1 -xzf "ta-lib-${TA_LIB_VERSION}-src.tar.gz" || { echo "Failed to extract TA-Lib source code"; exit 1; }

# Configure and build TA-Lib
./configure --prefix=/usr || { echo "Configuration failed"; exit 1; }
make || { echo "Build failed"; exit 1; }

echo "Installing TA-Lib globally..."
make install || { echo "Installation failed"; exit 1; }

# Check if the virtual environment exists
if [ -d "$VENV_DIR" ]; then
  echo "Virtual environment already exists in ${VENV_DIR}. Activating it..."
else
  # Create a new virtual environment
  echo "Creating a virtual environment in ${VENV_DIR}..."
  python3 -m venv "$VENV_DIR" || { echo "Failed to create virtual environment"; exit 1; }
  chmod -R 777 "$VENV_DIR" # Set permissions for the virtual environment
  VENV_CREATED=true  # Mark that the virtual environment was created by this script
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Installing TA-Lib Python wrapper in virtual environment..."
python3 -m pip install ta-lib || { echo "Failed to install TA-Lib Python wrapper"; exit 1; }

echo "Installing 'numpy<2.0.0' for compatibility with TA-Lib..."
python3 -m pip install 'numpy<2.0.0' || { echo "Failed to install 'numpy<2.0.0'"; exit 1; }

# Test the installation by importing talib in Python
echo "Testing TA-Lib installation..."
if python3 -c "import talib"; then
  echo "TA-Lib installed successfully in virtual environment"
else
  echo "ImportError detected. Exporting LD_LIBRARY_PATH or adding to ld.so.conf..."
  
  # Option 1: Export LD_LIBRARY_PATH (temporary for the session)
  export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
  
  # Option 2: Add /usr/local/lib to /etc/ld.so.conf and run ldconfig (permanent)
  echo "/usr/local/lib" | tee -a /etc/ld.so.conf
  /sbin/ldconfig
fi

echo "Deactivating virtual environment..."
deactivate

if $VENV_CREATED; then
  echo "Removing virtual environment created by the script..."
  rm -rf "$VENV_DIR"
fi

echo "TA-Lib C library installed globally, Python wrapper installed in virtual environment @ ${VENV_DIR}."
