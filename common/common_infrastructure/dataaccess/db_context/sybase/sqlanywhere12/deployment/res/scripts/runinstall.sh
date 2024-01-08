# iAnywhere Solutions, Inc. One Sybase Drive, Dublin, CA 94568, USA
# Copyright (c) 2001-2009, iAnywhere Solutions, Inc. Portions copyright (c) 
# 1988-2009, Sybase, Inc. All rights preserved. All unpublished rights reserved.

set_install_callback()
######################
{
    case "$1" in
	ERROR)
	    INSTALL_ERROR_CB="$2"
	    ;;
	QUESTION)
	    INSTALL_QUESTION_CB="$2"
	    ;;
	MESSAGE)
	    INSTALL_MESSAGE_CB="$2"
	    ;;
	STATUS)
	    INSTALL_STATUS_CB="$2"
	    ;;
	START)
	    INSTALL_STARTING_CB="$2"
	    ;;
	DONE)
	    INSTALL_DONE_CB="$2"
	    ;;
    esac
}

installer_message()
###################
{
    if [ -n "${INSTALL_MESSAGE_CB:-}" ] ; then
	eval `echo ${INSTALL_MESSAGE_CB} $*`
    fi
}

installer_status()
##################
{
    if [ -n "${INSTALL_STATUS_CB:-}" ] ; then
	eval `echo ${INSTALL_STATUS_CB} $*`
    fi
}

installer_error()
#################
{
    if [ -n "${INSTALL_ERROR_CB:-}" ] ; then
	eval `echo ${INSTALL_ERROR_CB} $*`
    fi
    signal_handler
}

installer_question()
####################
{
    if [ -n "${INSTALL_QUESTION_CB:-}" ] ; then
	eval `echo ${INSTALL_QUESTION_CB} \\"$*\\"`
    fi
}

installer_starting_install()
############################
{
    if [ -n "${INSTALL_STARTING_CB:-}" ] ; then
	eval `echo $INSTALL_STARTING_CB`
    fi
}

installer_done_install()
########################
{
    if [ -n "${INSTALL_DONE_CB:-}" ] ; then
	eval `echo $INSTALL_DONE_CB`
    fi
}

build_filelist()
################
{
    if [ -z "${INSTALL_FILELIST:-}" ]; then
        create_new_tmpfile
        INSTALL_FILELIST="${TMPFILE:-}"
    fi
 
    install_dir=`get_install_dir SA`
   
    echo dbinstall list -a -d "${install_dir:-}" -o \"`generate_package_mask`\" "$TICFILE" 1>&2
    eval dbinstall list -a -d "${install_dir:-}" -o \"`generate_package_mask`\" "$TICFILE" 2>&1 > "${INSTALL_FILELIST:-/dev/null}"
}

get_filelist()
##############
{
    if [ -z "${INSTALL_FILELIST:-}" ]; then
        build_filelist
    fi

    echo "${INSTALL_FILELIST:-}"
}

remove_old_jre()
################
# $1 dest directory
# $2 backup directory
{
    INST_DIR=${1:-}
    BACK_DIR=`echo "${2:-}" | sed -e 's/\(.*\)\/\(.*\)/\2/'`

    if [ -f ${INST_DIR}/sun/jre_1.6.0_linux_sun_i586/plugin/desktop/sun_java.desktop ] || [ -f ${INST_DIR}/sun/jre_1.6.0_linux_sun_x64/plugin/desktop/sun_java.desktop ]; then
        if [ -d ${INST_DIR}/sun/jre_1.6.0_linux_sun_x64 ]; then
            if [ ${BACK_DIR} = "null" ] ; then
                rm -rf $INST_DIR/sun/jre_1.6.0_linux_sun_x64
            else
                mv $INST_DIR/sun/jre_1.6.0_linux_sun_x64 $BACK_DIR/jre64
            fi
        fi
	if [ `plat_os` = "linux" ] && [ -d ${INST_DIR}/sun/jre_1.6.0_linux_sun_i586 ]; then
            if [ ${BACK_DIR} = "null" ] ; then
                rm -rf $INST_DIR/sun/jre_1.6.0_linux_sun_i586
            else
                mv $INST_DIR/sun/jre_1.6.0_linux_sun_i586 $BACK_DIR/jre32
            fi
        fi
    fi

}

restore_old_jre()
#################
# $1 dest directory
# $2 backup directory
{
    INST_DIR=${1:-}
    BACK_DIR=`echo "${2:-}" | sed -e 's/\(.*\)\/\(.*\)/\2/'`

    if [ -f ${BACK_DIR}/jre32/jre_1.6.0_linux_sun_i586/plugin/desktop/sun_java.desktop ] || [ -f ${BACK_DIR}/jre64/jre_1.6.0_linux_sun_x64/plugin/desktop/sun_java.desktop ]; then
        if [ -d ${BACK_DIR}/jre64 ]; then
            rm -rf $INST_DIR/sun/jre_1.6.0_linux_sun_x64
            mv $BACK_DIR/jre64/jre_1.6.0_linux_sun_x64 $INST_DIR/sun
        fi
        if [ -d ${BACK_DIR}/jre32 ]; then
            rm -rf $INST_DIR/sun/jre_1.6.0_linux_sun_i586
            mv $BACK_DIR/jre32/jre_1.6.0_linux_sun_i586 $INST_DIR/sun
        fi
    fi
}

remove_old_ssl()
################
# $1 dest directory
# $2 backup directory
{
    INST_DIR=${1:-}
    BACK_DIR=`echo "${2:-}" | sed -e 's/\(.*\)\/\(.*\)/\2/'`

    if [ -f ${INST_DIR}/lib32/libsbgse2.so ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f $INST_DIR/lib32/libsbgse2.so
        else
            mkdir -p $BACK_DIR/ssl32
            mv $INST_DIR/lib32/libsbgse2.so $BACK_DIR/ssl32/
        fi
    fi
    if [ -f ${INST_DIR}/lib64/libsbgse2.so ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f $INST_DIR/lib64/libsbgse2.so
        else
            mkdir -p $BACK_DIR/ssl64
            mv $INST_DIR/lib64/libsbgse2.so $BACK_DIR/ssl64/
        fi
    fi

}

restore_old_ssl()
#################
# $1 dest directory
# $2 backup directory
{
    INST_DIR=${1:-}
    BACK_DIR=`echo "${2:-}" | sed -e 's/\(.*\)\/\(.*\)/\2/'`

    if [ -f ${BACK_DIR}/ssl32/libsbgse2.so ]; then
        mv $BACK_DIR/ssl32/libsbgse2.so $INST_DIR/lib32/
    fi
    if [ -f ${BACK_DIR}/ssl64/libsbgse2.so ]; then
        mv $BACK_DIR/ssl64/libsbgse2.so $INST_DIR/lib64/
    fi
}

remove_old_ecc()
################
# $1 dest directory
# $2 backup directory
{
    INST_DIR=${1:-}
    BACK_DIR=`echo "${2:-}" | sed -e 's/\(.*\)\/\(.*\)/\2/'`

    SOVER=".1"
    if [ `plat_os` = "aix" ] ; then
        SOVER=""
    fi

    if [ `plat_os` = "linux" ] ; then
    ECC_FILE="libulecc.a"
    if [ -f ${INST_DIR}/ultralite/linux/x86/586/lib/${ECC_FILE} ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f ${INST_DIR}/ultralite/linux/x86/586/lib/${ECC_FILE}
        else
            mkdir -p $BACK_DIR/lib32
            mv ${INST_DIR}/ultralite/linux/x86/586/lib/${ECC_FILE} $BACK_DIR/lib32/
        fi
    fi
    fi

    ECC_FILE="eccserver.id"
    if [ -f ${INST_DIR}/bin32/${ECC_FILE} ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f ${INST_DIR}/bin32/${ECC_FILE}
        else
            mkdir -p $BACK_DIR/bin32
            mv ${INST_DIR}/bin32/${ECC_FILE} $BACK_DIR/bin32/
        fi
    fi
    if [ -f ${INST_DIR}/bin64/${ECC_FILE} ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f ${INST_DIR}/bin64/${ECC_FILE}
        else
            mkdir -p $BACK_DIR/bin64
            mv ${INST_DIR}/bin64/${ECC_FILE} $BACK_DIR/bin64/
        fi
    fi

    ECC_FILE="eccroot.crt"
    if [ -f ${INST_DIR}/bin32/${ECC_FILE} ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f ${INST_DIR}/bin32/${ECC_FILE}
        else
            mkdir -p $BACK_DIR/bin32
            mv ${INST_DIR}/bin32/${ECC_FILE} $BACK_DIR/bin32/
        fi
    fi
    if [ -f ${INST_DIR}/bin64/${ECC_FILE} ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f ${INST_DIR}/bin64/${ECC_FILE}
        else
            mkdir -p $BACK_DIR/bin64
            mv ${INST_DIR}/bin64/${ECC_FILE} $BACK_DIR/bin64/
        fi
    fi

    ECC_FILE="libmlecc_tls12_r.so"
    if [ -f ${INST_DIR}/lib32/${ECC_FILE}${SOVER} ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f ${INST_DIR}/lib32/${ECC_FILE}
            rm -f ${INST_DIR}/lib32/${ECC_FILE}.1
        else
            mkdir -p $BACK_DIR/lib32
            mv ${INST_DIR}/lib32/${ECC_FILE} $BACK_DIR/lib32/
            if [ `plat_os` != "aix" ] ; then
                mv ${INST_DIR}/lib32/${ECC_FILE}.1 $BACK_DIR/lib32/
            fi
        fi
    fi
    if [ -f ${INST_DIR}/lib64/${ECC_FILE}${SOVER} ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f ${INST_DIR}/lib64/${ECC_FILE}
            rm -f ${INST_DIR}/lib64/${ECC_FILE}.1
        else
            mkdir -p $BACK_DIR/lib64
            mv ${INST_DIR}/lib64/${ECC_FILE} $BACK_DIR/lib64/
            if [ `plat_os` != "aix" ] ; then
                mv ${INST_DIR}/lib64/${ECC_FILE}.1 $BACK_DIR/lib64/
            fi
        fi
    fi

    ECC_FILE="libmlcecc12_r.so"
    if [ -f ${INST_DIR}/lib32/${ECC_FILE}${SOVER} ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f ${INST_DIR}/lib32/${ECC_FILE}
            rm -f ${INST_DIR}/lib32/${ECC_FILE}.1
        else
            mkdir -p $BACK_DIR/lib32
            mv ${INST_DIR}/lib32/${ECC_FILE} $BACK_DIR/lib32/
            if [ `plat_os` != "aix" ] ; then
                mv ${INST_DIR}/lib32/${ECC_FILE}.1 $BACK_DIR/lib32/
            fi
        fi
    fi
    if [ -f ${INST_DIR}/lib64/${ECC_FILE}${SOVER} ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f ${INST_DIR}/lib64/${ECC_FILE}
            rm -f ${INST_DIR}/lib64/${ECC_FILE}.1
        else
            mkdir -p $BACK_DIR/lib64
            mv ${INST_DIR}/lib64/${ECC_FILE} $BACK_DIR/lib64/
            if [ `plat_os` != "aix" ] ; then
                mv ${INST_DIR}/lib64/${ECC_FILE}.1 $BACK_DIR/lib64/
            fi
        fi
    fi

    ECC_FILE="libdbcecc12_r"
    if [ -f ${INST_DIR}/lib32/${ECC_FILE}.so${SOVER} ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f ${INST_DIR}/lib32/${ECC_FILE}.so
            rm -f ${INST_DIR}/lib32/${ECC_FILE}.so.1
        else
            mkdir -p $BACK_DIR/lib32
            mv ${INST_DIR}/lib32/${ECC_FILE}.so $BACK_DIR/lib32/
            if [ `plat_os` != "aix" ] ; then
                mv ${INST_DIR}/lib32/${ECC_FILE}.so.1 $BACK_DIR/lib32/
            fi
        fi
    fi
    if [ -f ${INST_DIR}/lib64/${ECC_FILE}.so${SOVER} ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f ${INST_DIR}/lib64/${ECC_FILE}.so
            rm -f ${INST_DIR}/lib64/${ECC_FILE}.so.1
        else
            mkdir -p $BACK_DIR/lib64
            mv ${INST_DIR}/lib64/${ECC_FILE}.so $BACK_DIR/lib64/
            if [ `plat_os` != "aix" ] ; then
                mv ${INST_DIR}/lib64/${ECC_FILE}.so.1 $BACK_DIR/lib64/
            fi
        fi
    fi

    ECC_FILE="libdbecc12"
    if [ -f ${INST_DIR}/lib32/${ECC_FILE}.so${SOVER} ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f ${INST_DIR}/lib32/${ECC_FILE}.so
            rm -f ${INST_DIR}/lib32/${ECC_FILE}.so.1
            rm -f ${INST_DIR}/lib32/${ECC_FILE}_r.so
            rm -f ${INST_DIR}/lib32/${ECC_FILE}_r.so.1
        else
            mkdir -p $BACK_DIR/lib32
            mv ${INST_DIR}/lib32/${ECC_FILE}.so $BACK_DIR/lib32/
            mv ${INST_DIR}/lib32/${ECC_FILE}_r.so $BACK_DIR/lib32/
            if [ `plat_os` != "aix" ] ; then
                mv ${INST_DIR}/lib32/${ECC_FILE}.so.1 $BACK_DIR/lib32/
                mv ${INST_DIR}/lib32/${ECC_FILE}_r.so.1 $BACK_DIR/lib32/
            fi
        fi
    fi
    if [ -f ${INST_DIR}/lib64/${ECC_FILE}.so${SOVER} ] ; then
        if [ ${BACK_DIR} = "null" ] ; then
            rm -f ${INST_DIR}/lib64/${ECC_FILE}.so
            rm -f ${INST_DIR}/lib64/${ECC_FILE}.so.1
            rm -f ${INST_DIR}/lib64/${ECC_FILE}_r.so
            rm -f ${INST_DIR}/lib64/${ECC_FILE}_r.so.1
        else
            mkdir -p $BACK_DIR/lib64
            mv ${INST_DIR}/lib64/${ECC_FILE}.so $BACK_DIR/lib64/
            mv ${INST_DIR}/lib64/${ECC_FILE}_r.so $BACK_DIR/lib64/
            if [ `plat_os` != "aix" ] ; then
                mv ${INST_DIR}/lib64/${ECC_FILE}.so.1 $BACK_DIR/lib64/
                mv ${INST_DIR}/lib64/${ECC_FILE}_r.so.1 $BACK_DIR/lib64/
            fi
        fi
    fi

}

restore_old_ecc()
#################
# $1 dest directory
# $2 backup directory
{
    INST_DIR=${1:-}
    BACK_DIR=`echo "${2:-}" | sed -e 's/\(.*\)\/\(.*\)/\2/'`

    SOVER=".1"
    if [ `plat_os` = "aix" ] ; then
        SOVER=""
    fi

    ECC_FILE="libulecc.a"
    if [ -f ${BACK_DIR}/lib32/${ECC_FILE} ]; then
        mv ${BACK_DIR}/lib32/${ECC_FILE} $INST_DIR/ultralite/linux/x86/586/lib/
    fi

    ECC_FILE="eccserver.id"
    if [ -f ${BACK_DIR}/bin32/${ECC_FILE} ]; then
        mv ${BACK_DIR}/bin32/${ECC_FILE} $INST_DIR/bin32/
    fi
    if [ -f ${BACK_DIR}/bin64/${ECC_FILE} ]; then
        mv ${BACK_DIR}/bin64/${ECC_FILE} $INST_DIR/bin64/
    fi

    ECC_FILE="eccroot.crt"
    if [ -f ${BACK_DIR}/bin32/${ECC_FILE} ]; then
        mv ${BACK_DIR}/bin32/${ECC_FILE} $INST_DIR/bin32/
    fi
    if [ -f ${BACK_DIR}/bin64/${ECC_FILE} ]; then
        mv ${BACK_DIR}/bin64/${ECC_FILE} $INST_DIR/bin64/
    fi

    ECC_FILE="libmlecc_tls12_r.so"
    if [ -f ${BACK_DIR}/lib32/${ECC_FILE}${SOVER} ]; then
        mv ${BACK_DIR}/lib32/${ECC_FILE} $INST_DIR/lib32/
        if [ `plat_os` != "aix" ] ; then
            mv ${BACK_DIR}/lib32/${ECC_FILE}.1 $INST_DIR/lib32/
        fi
    fi
    if [ -f ${BACK_DIR}/lib64/${ECC_FILE}${SOVER} ]; then
        mv ${BACK_DIR}/lib64/${ECC_FILE} $INST_DIR/lib64/
        if [ `plat_os` != "aix" ] ; then
            mv ${BACK_DIR}/lib64/${ECC_FILE}.1 $INST_DIR/lib64/
        fi
    fi

    ECC_FILE="libmlcecc12_r.so"
    if [ -f ${BACK_DIR}/lib32/${ECC_FILE}${SOVER} ]; then
        mv ${BACK_DIR}/lib32/${ECC_FILE} $INST_DIR/lib32/
        if [ `plat_os` != "aix" ] ; then
            mv ${BACK_DIR}/lib32/${ECC_FILE}.1 $INST_DIR/lib32/
        fi
    fi
    if [ -f ${BACK_DIR}/lib64/${ECC_FILE}${SOVER} ]; then
        mv ${BACK_DIR}/lib64/${ECC_FILE} $INST_DIR/lib64/
        if [ `plat_os` != "aix" ] ; then
            mv ${BACK_DIR}/lib64/${ECC_FILE}.1 $INST_DIR/lib64/
        fi
    fi

    ECC_FILE="libdbcecc12"
    if [ -f ${BACK_DIR}/lib32/${ECC_FILE}.so${SOVER} ]; then
        mv ${BACK_DIR}/lib32/${ECC_FILE}.so $INST_DIR/lib32/
        mv ${BACK_DIR}/lib32/${ECC_FILE}_r.so $INST_DIR/lib32/
        if [ `plat_os` != "aix" ] ; then
            mv ${BACK_DIR}/lib32/${ECC_FILE}.so.1 $INST_DIR/lib32/
            mv ${BACK_DIR}/lib32/${ECC_FILE}_r.so.1 $INST_DIR/lib32/
        fi
    fi
    if [ -f ${BACK_DIR}/lib64/${ECC_FILE}.so${SOVER} ]; then
        mv ${BACK_DIR}/lib64/${ECC_FILE}.so $INST_DIR/lib64/
        mv ${BACK_DIR}/lib64/${ECC_FILE}_r.so $INST_DIR/lib64/
        if [ `plat_os` != "aix" ] ; then
            mv ${BACK_DIR}/lib64/${ECC_FILE}.so.1 $INST_DIR/lib64/
            mv ${BACK_DIR}/lib64/${ECC_FILE}_r.so.1 $INST_DIR/lib64/
        fi
    fi

}

do_install()
############
{
    install_dir=`get_install_dir SA`

    if not create_directory "$install_dir" ; then
  	installer_error "$install_dir"
    fi

    rollback_safe_start

    run_pre_install_actions

    extract_files "$install_dir"
    
    # Flow-specific actions
    run_install_actions

    run_post_install_actions

    rollback_safe_end
}

generate_install_file_name()
############################
{
    LF_DATESTAMP="`date +%Y%m%d-%H%M`"
    LF_PATHPREFIX=""

    if is_upgrade; then
	LF_LOGTYPE="upgrade"
    else
	LF_LOGTYPE="install"
    fi
    
    # On Mac OS X, avoid putting log file in top-level directory.
    if [ "`plat_os`" = "macos" ]; then
        LF_PATHPREFIX="System/"
	mkdir -p $LF_PATHPREFIX
    fi
    
    echo "${LF_PATHPREFIX}${LF_LOGTYPE}_${LF_DATESTAMP}"
}

extract_files()
################
# $1 dest directory
{
    pushd_quiet "$1"
    installer_status `msg_installing_files_into "${1}"`
    INSTALL_FILE=`generate_install_file_name`
    LOG_FILE="${INSTALL_FILE}.log"
    BACKUP_DIR="`dirname ${INSTALL_FILE}`/.`basename ${INSTALL_FILE}`"

    OPT_EXTRA="0"

    if [ `get_ui_type` = "silent" ] ; then
	OUTPUT=">/dev/null"
    else
	OUTPUT=""
    fi

    if is_upgrade ; then
        mkdir -p ${BACKUP_DIR}
        remove_old_jre "$install_dir" "${BACKUP_DIR}"
        remove_old_ssl "$install_dir" "${BACKUP_DIR}"
        remove_old_ecc "$install_dir" "${BACKUP_DIR}"
        push_rollback_callback rollback_extracted_files \""$1"\" \""${BACKUP_DIR}"\" \""${LOG_FILE}"\"
        push_cleanup_callback cleanup_backup_files \""$1"\" \""${BACKUP_DIR}"\"
	SWITCHES="-d '$1' -b '${BACKUP_DIR}'"
    else
        remove_old_jre "$install_dir" "/dev/null"
        remove_old_ssl "$install_dir" "/dev/null"
        remove_old_ecc "$install_dir" "/dev/null"
	SWITCHES="-k `get_registration_key`"
    fi

    installer_starting_install
    eval dbinstall install $SWITCHES -o \"`generate_package_mask`\" -l "$LOG_FILE" "$TICFILE" 2>&1 $OUTPUT
    installer_done_install

    sleep 1

    SUCCESS=`sed '$!d' "$LOG_FILE"`
    if [ "$SUCCESS" != "ok" ] ; then
	# something went wrong
	L_DIR=`pwd`
	installer_error `msg_error_extracting_files "${1}" "${L_DIR}/${LOG_FILE}"`
    else
	installer_message "$MSG_COMPLETED"
	installer_message `msg_extracted_files_location "${LOG_FILE}" "${1}"`
	if [ `plat_os` = "aix" ]; then
	    # On AIX 5.3 TL06, must unset execute bits on shared objects, otherwise they crash on load
	    chmod a-x `echo "${1}/*/*.so"`
	fi
	# If we've overwritten pre-installed DBs, clean up the old log files here
	if has_feature SAMPLES ; then
            if is_upgrade && [ -f "`get_install_dir SA`/demo.log" ] ; then
	        mv "`get_install_dir SA`/demo.log" "${BACKUP_DIR}/demo.log"
            else
	        rm -f "`get_install_dir SA`/demo.log"
            fi
	fi
	if has_feature SAMON ; then
            if is_upgrade && [ -f "`get_install_dir SA`/samonitor.log" ] ; then
	        mv "`get_install_dir SA`/samonitor.log" "${BACKUP_DIR}/samonitor.log"
            else
	        rm -f "`get_install_dir SA`/samonitor.log"
            fi
	fi
    fi
    popd_quiet
}

rollback_extracted_files()
##########################
# $1 dest directory
# $2 backup directory
{
    INSTALL_DIR=${1:-}
    BACKUP_DIR=${2:-}
    LOG_FILE=${3:-}
    PREV_LINE_LENGTH=0

    if [ -n "${INSTALL_DIR:-}" ] && [ -d "${INSTALL_DIR:-}" ] ; then
        pushd_quiet "${INSTALL_DIR:-}"
        if [ -n "${BACKUP_DIR:-}" ] && [ -d "${BACKUP_DIR:-}" ] ; then
            installer_status `msg_reverting_files_into "${1:-}"`
            
            TOTAL_NUM_FILES=`wc -l ${LOG_FILE} | cut -d ' ' -f 1`
            CURRENT_FILE=0

            installer_starting_install
            for file in `cut -c 23- ${LOG_FILE}` demo.log; do
                if [ `get_ui_type` != "silent" ] ; then
		    CURRENT_PERCENT=`expr \( $CURRENT_FILE \* 100 \) / $TOTAL_NUM_FILES`
                    CURRENT_FILE=`expr $CURRENT_FILE + 1`

                    LINE=" "
                    if [ ${CURRENT_PERCENT:-0} -lt 10 ]; then
                        LINE=" ${LINE}"
                    fi
                    LINE="${LINE}${CURRENT_PERCENT}% ${file}"
                    LINE_LENGTH=`echo ${LINE} | wc -c`
                
                    echo -n "${LINE:-}"
                
                    LAST_LINE_LENGTH=`expr ${LAST_LINE_LENGTH:-0} - ${LINE_LENGTH:-0}`
                    while [ ${LAST_LINE_LENGTH:-0} -gt 0 ]; do
                        echo -n ' '
                        LAST_LINE_LENGTH=`expr ${LAST_LINE_LENGTH:-0} - 1`
                    done
                    echo -n -e "\r"
                
                    LAST_LINE_LENGTH=`echo ${LINE} | wc -c`
                fi

                BACKUP_FILE="${BACKUP_DIR}/${file}"
                if [ -f "${BACKUP_FILE}" ] || [ -L "${BACKUP_FILE}" ]; then
                    rm -f "${file}"
                    if [ -L "${BACKUP_FILE}" ] || \
                        [ "`wc -l ${BACKUP_FILE} 2>/dev/null`" != "1 ${BACKUP_FILE}" ] || \
                        [ "`grep "created as ${BACKUP_FILE}" ${BACKUP_FILE} 2>/dev/null`" != "created as ${file}" ] ; then
                        mv "${BACKUP_FILE}" "${file}"
                    fi
                fi
            done
            if [ `get_ui_type` != "silent" ] ; then
                while [ ${LAST_LINE_LENGTH:-0} -gt 0 ]; do
                    echo -n ' '
                    LAST_LINE_LENGTH=`expr ${LAST_LINE_LENGTH:-0} - 1`
                done
                echo -n -e "\r"
            fi

            restore_old_ecc ${INSTALL_DIR} ${BACKUP_DIR}
            restore_old_ssl ${INSTALL_DIR} ${BACKUP_DIR}
            restore_old_jre ${INSTALL_DIR} ${BACKUP_DIR}

            installer_done_install
        fi
        popd_quiet
    fi
}

cleanup_backup_files()
######################
# $1 dest directory
# $2 backup directory
{
    INSTALL_DIR=${1:-}
    BACKUP_DIR=${2:-}
    if [ -n "${INSTALL_DIR:-}" ] && [ -d "${INSTALL_DIR:-}" ] ; then
        pushd_quiet "${INSTALL_DIR:-}"
        if [ -n "${BACKUP_DIR:-}" ] && [ -d "${BACKUP_DIR:-}" ] ; then
            rm -rf "${BACKUP_DIR:-}"
        fi
        popd_quiet
    fi
}

get_install_mode()
##################
{
    if [ -z "${__INSTALL_MODE:-}" ]; then
        if [ `get_install_type` = "EBF" ] ||
            [ `get_install_type` = "EBF_SAMON" ] ||
            [ `get_install_type` = "EBF_DBCLOUD" ]; then
            set_install_mode "UPGRADE"
        else
            set_install_mode "CREATE"
        fi
    fi

    echo ${__INSTALL_MODE:-}
}

is_create()
###########
{
    [ `get_install_mode` = "CREATE" ] && not is_addon_key
}

is_modify()
###########
{
    [ `get_install_mode` = "MODIFY" ] || (
        [ `get_install_mode` = "CREATE" ] && is_addon_key )
}

is_upgrade()
############
{
    [ `get_install_mode` = "UPGRADE" ]
}

set_install_mode()
##################
{
    __INSTALL_MODE=`toupper ${1:-CREATE}`
}

set_install_action_function()
#############################
{
    __INSTALL_ACTION_FN="$1"
}

run_install_actions()
#####################
{
    if [ -n "${__INSTALL_ACTION_FN:-}" ]; then
	$__INSTALL_ACTION_FN
    fi
}

set_pre_install_action_function()
#################################
{
    __PRE_INSTALL_ACTION_FN="$1"
}

run_pre_install_actions()
#########################
{
    if [ -n "${__PRE_INSTALL_ACTION_FN:-}" ]; then
	$__PRE_INSTALL_ACTION_FN
    fi
}

set_post_install_action_function()
##################################
{
    __POST_INSTALL_ACTION_FN="$1"
}

run_post_install_actions()
##########################
{
    if [ -n "${__POST_INSTALL_ACTION_FN:-}" ]; then
	$__POST_INSTALL_ACTION_FN
    fi
}

selinux_setup()
###############
{
    if [ `plat_os` = "linux" ] ; then
	find "`get_install_dir SA`" -name "*.so" | xargs chcon -t textrel_shlib_t 2>/dev/null
	
	if has_feature SELINUX ; then
	    pushd_quiet "`get_install_dir SA`/selinux"
	    /bin/sh buildfc.sh "`get_install_dir SA`"
	    popd_quiet
	fi
    fi
}
