#!/bin/bash
# Quick start script for Graph Creator with automatic setup

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
VENV_DIR="venv"
PYTHON_MIN_VERSION="3.11"
MARKER_FILE=".setup_complete"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Graph Creator - Startup Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to check Python version
check_python_version() {
    echo -e "${BLUE}[1/5] Checking Python version...${NC}"
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Error: python3 not found. Please install Python 3.11 or higher.${NC}"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    
    if [ "$(printf '%s\n' "$PYTHON_MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$PYTHON_MIN_VERSION" ]; then
        echo -e "${RED}Error: Python $PYTHON_MIN_VERSION or higher required. Found: $PYTHON_VERSION${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"
    echo ""
}

# Function to create virtual environment
create_venv() {
    echo -e "${BLUE}[2/5] Checking virtual environment...${NC}"
    
    if [ -d "$VENV_DIR" ]; then
        echo -e "${GREEN}✓ Virtual environment already exists${NC}"
    else
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv "$VENV_DIR"
        echo -e "${GREEN}✓ Virtual environment created${NC}"
    fi
    echo ""
}

# Function to activate virtual environment
activate_venv() {
    echo -e "${BLUE}[3/5] Activating virtual environment...${NC}"
    
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
        echo -e "${GREEN}✓ Virtual environment activated${NC}"
    else
        echo -e "${RED}Error: Virtual environment activation script not found${NC}"
        exit 1
    fi
    echo ""
}

# Function to install dependencies
install_dependencies() {
    echo -e "${BLUE}[4/5] Checking dependencies...${NC}"
    
    # Check if we need to install
    NEED_INSTALL=0
    
    if [ ! -f "$MARKER_FILE" ]; then
        NEED_INSTALL=1
    elif ! python -c "import flet" 2>/dev/null; then
        NEED_INSTALL=1
    fi
    
    if [ $NEED_INSTALL -eq 1 ]; then
        echo -e "${YELLOW}Installing dependencies (this may take a few minutes)...${NC}"
        
        # Upgrade pip first
        pip install --upgrade pip > /dev/null 2>&1
        
        # Install the package in editable mode
        pip install -e . || {
            echo -e "${RED}Error: Failed to install dependencies${NC}"
            exit 1
        }
        
        # Create marker file
        date > "$MARKER_FILE"
        
        echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
    else
        echo -e "${GREEN}✓ Dependencies already installed${NC}"
    fi
    echo ""
}

# Function to run the application
run_application() {
    echo -e "${BLUE}[5/5] Starting Graph Creator...${NC}"
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Application is starting...${NC}"
    echo -e "${GREEN}Press Ctrl+C to exit${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    
    # Disable telemetry
    export FLET_TELEMETRY_DISABLED=1
    
    # Run the application
    python -m app.main
}

# Main execution flow
main() {
    check_python_version
    create_venv
    activate_venv
    install_dependencies
    run_application
}

# Handle script arguments
case "${1:-}" in
    --clean)
        echo -e "${YELLOW}Cleaning setup (removing venv and marker)...${NC}"
        rm -rf "$VENV_DIR" "$MARKER_FILE"
        echo -e "${GREEN}✓ Clean complete. Run ./run.sh to reinstall.${NC}"
        exit 0
        ;;
    --reinstall)
        echo -e "${YELLOW}Forcing reinstall of dependencies...${NC}"
        rm -f "$MARKER_FILE"
        main
        ;;
    --help|-h)
        echo "Usage: ./run.sh [OPTION]"
        echo ""
        echo "Options:"
        echo "  (no args)      Run the application (install if needed)"
        echo "  --clean        Remove virtual environment and setup marker"
        echo "  --reinstall    Force reinstall of dependencies"
        echo "  --help, -h     Show this help message"
        echo ""
        exit 0
        ;;
    "")
        main
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        echo "Run './run.sh --help' for usage information"
        exit 1
        ;;
esac

