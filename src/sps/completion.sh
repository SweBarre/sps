SPS_COMPLETE="\
    package\
    product\
    completion\
    patchproduct\
    patch\
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
    --sort-table\
    --no-borders\
    --no-header"

SPS_PRODUCT_SORT_TABLE_COMPLETE="\
    id\
    Name\
    Edition\
    Identifier\
    Arch"

SPS_PACKAGE_PRODUCT_COMPLETE="{sps_package_product_complete}"

SPS_COMPLETION_COMLPETE="\
    bash\
    --help"

SPS_PACKAGE_COMPLETE="\
    --exact-match\
    --cache-age\
    --cache-file\
    --sort-table\
    --no-borders\
    --no-header\
    --version\
    --help"

SPS_PACKAGE_SORT_TABLE_COMPLETE="\
    Name\
    Version\
    Release\
    Arch\
    Module"


SPS_PATCHPRODUCT_COMPLETE="\
    --cache-age\
    --cache-file\
    --update-cache\
    --no-cache\
    --help\
    --version\
    --sort-table\
    --no-borders\
    --no-header"

SPS_PATCHPRODUCT_SORT_TABLE_COMPLETE="\
    Name\
    Version\
    Arch\
    id"

SPS_PATCH_PRODUCT_COMPLETE="{sps_patch_product_complete}"
SPS_PATCH_ARCH_COMPLETE="{sps_patch_arch_complete}"
SPS_PATCH_VERSION_COMPLETE="{sps_patch_version_complete}"

SPS_PATCH_COMPLETE="\
    --help\
    --cache-file\
    --cache-age\
    --version\
    --severity\
    --only-security-patches\
    --date-from\
    --date-to\
    --page\
    --sort-table\
    --product\
    --arch\
    --product-version\
    --detail\
    --no-borders\
    --no-header"

SPS_PATCH_SEVERITY_COMPLETE="\
    all\
    lov\
    moderate\
    important\
    critical"

SPS_PATCH_SORT_TABLE_COMPLETE="\
    Severity\
    Name\
    Product\
    Arch\
    id\
    Released"

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
        patchproduct)
            case "${prev}" in
                patchproduct)
                    suggestions=""
                    ;;
                --sort-table)
                    suggestions="$SPS_PATCHPRODUCT_SORT_TABLE_COMPLETE"
                    ;;
                --cache-file)
                    suggestions=""
                    ;;
                --cache-age)
                    suggestions=""
                    ;;
                *)
                    suggestions="$SPS_PATCHPRODUCT_COMPLETE"
                    ;;
            esac
            ;;
        patch)
            case "${prev}" in
                patch)
                    suggestions=""
                    ;;
                --severity)
                    suggestions="$SPS_PATCH_SEVERITY_COMPLETE"
                    ;;
                --date-from)
                    suggestions=""
                    ;;
                --date-to)
                    suggestions=""
                    ;;
                --page)
                    suggestions=""
                    ;;
                --product)
                    suggestions="$SPS_PATCH_PRODUCT_COMPLETE"
                    ;;
                --arch)
                    suggestions="$SPS_PATCH_ARCH_COMPLETE"
                    ;;
                --product-version)
                    suggestions="$SPS_PATCH_VERSION_COMPLETE"
                    ;;
                --sort-table)
                    suggestions="$SPS_PATCH_SORT_TABLE_COMPLETE"
                    ;;
                *)
                    suggestions="$SPS_PATCH_COMPLETE"
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
           [[ ! "---arch -A --product-version -V --product -p -C --cache-file -S --sort-table -a --cache-age --severity -e --date-from -f --date-to -t" =~ "${COMP_WORDS[i-1]}" ]]; then
            firstword=${COMP_WORDS[i]}
            break
        fi
    done
    echo $firstword
}

complete -F _sps_complete sps
