PATH_LIDC_IDRI=$1
OUTPUT_DIR_PATH=$2

mkdir -p "${OUTPUT_DIR_PATH}"


# download cycle
wget -P "${OUTPUT_DIR_PATH}" "https://www.grip.unina.it/download/prog/M3Dsynth/cycle.tgz"
tar -xzvf "${OUTPUT_DIR_PATH}/cycle.tgz" --directory "${OUTPUT_DIR_PATH}"


# download pix2pix
wget -P "${OUTPUT_DIR_PATH}" "https://www.grip.unina.it/download/prog/M3Dsynth/pix2pix.tgz"
tar -xzvf "${OUTPUT_DIR_PATH}/pix2pix.tgz" --directory "${OUTPUT_DIR_PATH}"


# download diffusion
wget -P "${OUTPUT_DIR_PATH}" "https://www.grip.unina.it/download/prog/M3Dsynth/diffusion.tgz"
tar -xzvf "${OUTPUT_DIR_PATH}/diffusion.tgz" --directory "${OUTPUT_DIR_PATH}"



# convert real to tiff
python convert_real_to_tiff.py "${PATH_LIDC_IDRI}" "${OUTPUT_DIR_PATH}"
