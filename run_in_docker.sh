#!/usr/bin/env bash
printf "Running scriptlet\n"
set -e
set -x

# shellcheck disable=SC2046
DIRECTORY=$(dirname $(readlink -e "$0"))

cd "${DIRECTORY}"

export PYTHONPATH="$DIRECTORY:$DIRECTORY/src:$DIRECTORY/src/DaoNodeUnit:$DIRECTORY/src/AdditionalPackages:$DIRECTORY/src/DaoNodeUnit:$DIRECTORY/src/DaoWorkers:$DIRECTORY/src/DaoWorkersSpecifications:$DIRECTORY/src/DevelopToolBox:$DIRECTORY/src/DomainService:$DIRECTORY/src/Global:$DIRECTORY/src/Global2p1:$DIRECTORY/src/Global2p2:$DIRECTORY/src/Global2p3:$DIRECTORY/src/GraphAnalytics:$DIRECTORY/src/LibByzaticCommon:$DIRECTORY/src/NodeDescriptionManager:$DIRECTORY/src/NodeUnitIterator:$DIRECTORY/src/NodeUnitRepository:$DIRECTORY/src/ServicePrometheus:$DIRECTORY/src/StorageManager:$DIRECTORY/src/WorkersManager:$DIRECTORY/src/WorkersRepository"
python ./main.py