#!/usr/bin/env python3
#
# QUERIES <<-- (developer test version)
#

# filesystem
PROMETHEUS_QUERY_1 = \
    "((((((100 - ((node_filesystem_avail_bytesTAGLINEPLACEHOLDER * 100) / node_filesystem_size_bytesTAGLINEPLACEHOLDER ))< bool LLIMITPLACEHOLDER)))-1)== 0)" + \
    "OR" + \
    "((((((100 - ((node_filesystem_avail_bytesTAGLINEPLACEHOLDER  * 100) / node_filesystem_size_bytesTAGLINEPLACEHOLDER ))> bool LLIMITPLACEHOLDER)" + \
    ")*(" + \
    "((100 - ((node_filesystem_avail_bytesTAGLINEPLACEHOLDER  * 100) / node_filesystem_size_bytesTAGLINEPLACEHOLDER ))< bool HLIMITPLACEHOLDER)))+0)== 1)" + \
    "OR" + \
    "((((((100 - ((node_filesystem_avail_bytesTAGLINEPLACEHOLDER  * 100) / node_filesystem_size_bytesTAGLINEPLACEHOLDER ))> bool HLIMITPLACEHOLDER)))+1)== 2)" + \
    "OR" + \
    " on() vector(1)"

# cpu
PROMETHEUS_QUERY_2 = \
    "((((((((count(count(node_cpu_seconds_totalTAGLINEPLACEHOLDER) by (cpu))) - avg(sum by (mode)(rate(node_cpu_seconds_totalTAGLINEPLACEHOLDER[30m])))) * 100) / count(count(node_cpu_seconds_totalTAGLINEPLACEHOLDER) by (cpu))< bool LLIMITPLACEHOLDER)))-1)== 0)" + \
    "OR" + \
    "((((((((count(count(node_cpu_seconds_totalTAGLINEPLACEHOLDER) by (cpu))) - avg(sum by (mode)(rate(node_cpu_seconds_totalTAGLINEPLACEHOLDER[30m])))) * 100) / count(count(node_cpu_seconds_totalTAGLINEPLACEHOLDER) by (cpu))> bool LLIMITPLACEHOLDER)" + \
    ")*(" + \
    "((((count(count(node_cpu_seconds_totalTAGLINEPLACEHOLDER) by (cpu))) - avg(sum by (mode)(rate(node_cpu_seconds_totalTAGLINEPLACEHOLDER[30m])))) * 100) / count(count(node_cpu_seconds_totalTAGLINEPLACEHOLDER) by (cpu))< bool HLIMITPLACEHOLDER)))+0)== 1)" + \
    "OR" + \
    "((((((((count(count(node_cpu_seconds_totalTAGLINEPLACEHOLDER) by (cpu))) - avg(sum by (mode)(rate(node_cpu_seconds_totalTAGLINEPLACEHOLDER[30m])))) * 100) / count(count(node_cpu_seconds_totalTAGLINEPLACEHOLDER) by (cpu))> bool HLIMITPLACEHOLDER)))+1)== 2)" + \
    "OR" + \
    " on() vector(1)"

# memory
PROMETHEUS_QUERY_3 = \
    "(((((((((node_memory_MemTotal_bytesTAGLINEPLACEHOLDER - node_memory_MemFree_bytesTAGLINEPLACEHOLDER) - node_memory_Cached_bytesTAGLINEPLACEHOLDER) / (node_memory_MemTotal_bytesTAGLINEPLACEHOLDER)) * 100)< bool LLIMITPLACEHOLDER)))-1)== 0)" + \
    "OR" + \
    "(((((((((node_memory_MemTotal_bytesTAGLINEPLACEHOLDER - node_memory_MemFree_bytesTAGLINEPLACEHOLDER) - node_memory_Cached_bytesTAGLINEPLACEHOLDER) / (node_memory_MemTotal_bytesTAGLINEPLACEHOLDER)) * 100)> bool LLIMITPLACEHOLDER)" + \
    ")*(" + \
    "(((((node_memory_MemTotal_bytesTAGLINEPLACEHOLDER - node_memory_MemFree_bytesTAGLINEPLACEHOLDER) - node_memory_Cached_bytesTAGLINEPLACEHOLDER) / (node_memory_MemTotal_bytesTAGLINEPLACEHOLDER)) * 100)< bool HLIMITPLACEHOLDER)))+0)== 1)" + \
    "OR" + \
    "(((((((((node_memory_MemTotal_bytesTAGLINEPLACEHOLDER - node_memory_MemFree_bytesTAGLINEPLACEHOLDER) - node_memory_Cached_bytesTAGLINEPLACEHOLDER) / (node_memory_MemTotal_bytesTAGLINEPLACEHOLDER)) * 100)> bool HLIMITPLACEHOLDER)))+1)== 2)" + \
    "OR" + \
    " on() vector(1)"

# swap
PROMETHEUS_QUERY_4 = \
    "((((((((node_memory_SwapTotal_bytesTAGLINEPLACEHOLDER - node_memory_SwapFree_bytesTAGLINEPLACEHOLDER) / (node_memory_SwapTotal_bytesTAGLINEPLACEHOLDER )) * 100)< bool LLIMITPLACEHOLDER)))-1)== 0)" + \
    "OR" + \
    "((((((((node_memory_SwapTotal_bytesTAGLINEPLACEHOLDER - node_memory_SwapFree_bytesTAGLINEPLACEHOLDER) / (node_memory_SwapTotal_bytesTAGLINEPLACEHOLDER )) * 100)> bool LLIMITPLACEHOLDER)" + \
    ")*(" + \
    "((((node_memory_SwapTotal_bytesTAGLINEPLACEHOLDER - node_memory_SwapFree_bytesTAGLINEPLACEHOLDER) / (node_memory_SwapTotal_bytesTAGLINEPLACEHOLDER )) * 100)< bool HLIMITPLACEHOLDER)))+0)== 1)" + \
    "OR" + \
    "((((((((node_memory_SwapTotal_bytesTAGLINEPLACEHOLDER - node_memory_SwapFree_bytesTAGLINEPLACEHOLDER) / (node_memory_SwapTotal_bytesTAGLINEPLACEHOLDER )) * 100)> bool HLIMITPLACEHOLDER)))+1)== 2)" + \
    "OR" + \
    " on() vector(1)"

# 
PROMETHEUS_QUERY_5 = \
    "(((host_avalability_checkerTAGLINEPLACEHOLDER)-0)== 0)" + \
    "OR" + \
    "(((host_avalability_checkerTAGLINEPLACEHOLDER)+1)== 2)" + \
    "OR" + \
    "(((host_avalability_checkerTAGLINEPLACEHOLDER)+1)== 3)" + \
    "OR" + \
    " on() vector(1)"

# 
PROMETHEUS_QUERY_6 = \
    "(metrics_core_rootTAGLINEPLACEHOLDER)" + \
    "OR" + \
    " on() vector(1)"

# 
PROMETHEUS_QUERY_7 = \
    "(metrics_core_installationTAGLINEPLACEHOLDER)" + \
    "OR" + \
    " on() vector(1)"

# 
PROMETHEUS_QUERY_8 = \
    "(metrics_core_hostTAGLINEPLACEHOLDER)" + \
    "OR" + \
    " on() vector(1)"

PROMETHEUS_QUERY_9 = \
    "(metrics_core_sourceTAGLINEPLACEHOLDER)" + \
    "OR" + \
    " on() vector(1)"

PROMETHEUS_QUERY_10 = \
    "(metrics_core_availabilityTAGLINEPLACEHOLDER)" + \
    "OR" + \
    " on() vector(1)"

PROMETHEUS_QUERY_11 = \
    "(installationTAGLINEPLACEHOLDER)" + \
    "OR" + \
    " on() vector(1)"

PROMETHEUS_QUERY_12 = \
    "((((((rate(node_disk_io_time_seconds_totalTAGLINEPLACEHOLDER[30m]) * 100) < bool LLIMITPLACEHOLDER)))-1)== 0)" + \
    "OR" + \
    "((((((rate(node_disk_io_time_seconds_totalTAGLINEPLACEHOLDER[30m]) * 100) > bool LLIMITPLACEHOLDER))*(((rate(node_disk_io_time_seconds_totalTAGLINEPLACEHOLDER[30m]) * 100) < bool HLIMITPLACEHOLDER)))+0)== 1)" + \
    "OR" + \
    "((((((rate(node_disk_io_time_seconds_totalTAGLINEPLACEHOLDER[30m]) * 100) > bool HLIMITPLACEHOLDER)))+1)== 2)" + \
    "OR" + \
    " on() vector(1)"

PROMETHEUS_QUERY_13 = \
    "(aggregation_mainTAGLINEPLACEHOLDER)" + \
    "OR" + \
    " on() vector(1)"

# LISTING
PROMETHEUS_QUERIES = {
    'filesystem': PROMETHEUS_QUERY_1,
    'cpu': PROMETHEUS_QUERY_2,
    'memory': PROMETHEUS_QUERY_3,
    'swap': PROMETHEUS_QUERY_4,
    'availability': PROMETHEUS_QUERY_5,
    'metrics_core_root': PROMETHEUS_QUERY_6,
    'metrics_core_installation': PROMETHEUS_QUERY_7,
    'metrics_core_host': PROMETHEUS_QUERY_8,
    'metrics_core_source': PROMETHEUS_QUERY_9,
    'metrics_core_availability': PROMETHEUS_QUERY_10,
    'installation': PROMETHEUS_QUERY_11,
    'disk_io_util': PROMETHEUS_QUERY_12,
    'aggregation_main': PROMETHEUS_QUERY_13
    }




