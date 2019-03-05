SPS_COMPLETE="\
    package\
    product\
    completion\
    --help"

SPS_PRODUCT_COMPLETE="\
    --field\
    --update-cache\
    --no-cache\
    --no-borders\
    --no-header\
    --short\
	--sort\
    --help"

SPS_PRODUCT_SORT_COMPLETE="\
	id\
	Name\
	Edition\
	Identifier\
	Arch"

SPS_PRODUCT_OPTION_FIELD_COMPLETE="\
    name\
    identifier\
    edition"

SPS_PACKAGE_COMPLETE="\
    --product\
	--sort\
    --help"

SPS_PACKAGE_SORT_COMLETE="\
	Name\
	Version\
	Release\
	Arch\
	Module"

if [[ -f ~/.cache/sps/products ]];then
	SPS_PACKAGE_PRODUCT_COMPLETE="$(sps product --short | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g')"
else
	SPS_PACKAGE_PRODUCT_COMPLETE=""
fi

SPS_COMPLETION_COMLPETE="\
	bash\
	--help"

_sps_complete()
{
	local cur prev firstword suggestions
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"
	firstword=$(_sps_get_firstword)

	case "${firstword}" in
		product)
			case "${prev}" in
				--field)
					suggestions="$SPS_PRODUCT_OPTION_FIELD_COMPLETE"
					;;
				--sort)
					suggestions="$SPS_PRODUCT_SORT_COMPLETE"
					;;
				*)
					suggestions="$SPS_PRODUCT_COMPLETE"
					;;
			esac
			;;
		package)
			case "${prev}" in
				--product)
					suggestions="$SPS_PACKAGE_PRODUCT_COMPLETE"
					;;
				--sort)
					suggestions="$SPS_PACKAGE_SORT_COMLETE"
					;;
				*)
					suggestions="$SPS_PACKAGE_COMPLETE"
					;;
			esac
			;;
		completion)
			suggestions="$SPS_COMPLETION_COMLPETE"
			;;
		*)
			suggestions="$SPS_COMPLETE"
			;;
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

	firstword=
	for ((i = 1; i < ${#COMP_WORDS[@]}; ++i)); do
		if [[ ${COMP_WORDS[i]} != -* ]]; then
			firstword=${COMP_WORDS[i]}
			break
		fi
	done
	echo $firstword
}

complete -F _sps_complete sps

