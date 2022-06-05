# Create root folder for testing and subfolders for log and data
if [[ "$1" ]];then
    ROOT_DIR=$1
else
   ROOT_DIR="test" 
fi
mkdir -p "${ROOT_DIR}" "${ROOT_DIR}/log" "${ROOT_DIR}/data" "${ROOT_DIR}/archive" "${ROOT_DIR}/temp" 
# Start python script
python3 main.py