SPS_COMPLETE="\
    package\
    product\
    completion\
    --help\
    --version\
    --cache-age\
    --cache-file"

SPS_PRODUCT_COMPLETE="\
    --cache-age\
    --cache-file\
    --update-cache\
    --no-cache\
    --help\
    --version\
    --short\
    --sort-table\
    --no-borders\
    --no-header"

SPS_PRODUCT_SORT_TABLE_COMPLETE="\
    id\
    Name\
    Edition\
    Identifier\
    Arch"


if [[ -f {sps_cachefile} ]];then
    SPS_PACKAGE_PRODUCT_COMPLETE="$(sps product --short | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g')"
else
    SPS_PACKAGE_PRODUCT_COMPLETE=""
fi

SPS_COMPLETION_COMLPETE="\
    bash\
    --help"

SPS_PACKAGE_COMPLETE="\
    --cache-age\
    --cache-file\
    --sort-table\
    --no-borders\
    --no-header\
    --help"

SPS_PACKAGE_SORT_TABLE_COMPLETE="\
    Name\
    Version\
    Release\
    Arch\
    Module"

_sps_complete()
{
    local cur prev firstword suggestions
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    firstword=$(_sps_get_firstword)

    case "${firstword}" in
        product)
            case "${prev}" in
                product)
                    suggestions=""
                    ;;
                --sort-table)
                    suggestions="$SPS_PRODUCT_SORT_TABLE_COMPLETE"
                    ;;
                --cache-file)
                    suggestions=""
                    ;;
                --cache-age)
                    suggestions=""
                    ;;
                *)
                    suggestions="$SPS_PRODUCT_COMPLETE"
                    ;;
            esac
            ;;
        package)
            case "${prev}" in
                package)
                    suggestions="$SPS_PACKAGE_PRODUCT_COMPLETE"
                    ;;
                --sort-table)
                    suggestions="$SPS_PACKAGE_SORT_TABLE_COMPLETE"
                    ;;
                --cache-file)
                    suggestions=""
                    ;;
                --cache-age)
                    suggestions=""
                    ;;
                *)
                    if [[ "${COMP_WORDS[COMP_CWORD-1]}" = "package" ]];then
                        suggestions=""
                    elif [[ "${COMP_WORDS[COMP_CWORD-2]}" = "package" ]];then
                        suggestions=""
                    else
                        suggestions="$SPS_PACKAGE_COMPLETE"
                    fi
                    ;;
            esac
            ;;
        completion)
            case "${prev}" in
                --cache-file)
                    suggestions=""
                    ;;
                --cache-age)
                    suggestions=""
                    ;;
                *)
                    suggestions="$SPS_COMPLETION_COMLPETE"
                ;;
            esac
            ;;
        *)
            case "${prev}" in
                --cache-file)
                    suggestions=""
                    ;;
                 --cache-age)
                    suggestions=""
                    ;;
                *)
                    suggestions="$SPS_COMPLETE"
                    ;;
            esac
    esac

    if [[ "${suggestions}x" == "x" ]];then
        COMPREPLY=()
    else
        COMPREPLY=( $(compgen -W "${suggestions}" -- ${cur}) )
    fi
    return 0
}

_sps_get_firstword() {
    local firstword i
    local dual_options


    firstword=
    for ((i = 1; i < ${#COMP_WORDS[@]}; ++i)); do
        if [[ ${COMP_WORDS[i]} != -* ]] && \
           [[ ! "-C --cache-file -S --sort-table -a --cache-age" =~ "${COMP_WORDS[i-1]}" ]]; then
            firstword=${COMP_WORDS[i]}
            break
        fi
    done
    echo $firstword
}

complete -F _sps_complete sps
