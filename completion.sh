_sps_complete()
{
	local cur prev firstword suggestions
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"
	firstword=$(_sps_get_firstword)


	SPS_COMPLETE="\
		package\
		product\
		--help"

	PRODUCT_COMPLETE="\
		--field\
		--update-cache\
		--no-cache\
		--no-borders\
		--no-header\
		--short\
		--help"

	PRODUCT_OPTION_FIELD_COMPLETE="\
		name\
		identifier\
		edition"

	PACKAGE_COMPLETE="\
		--product\
		--help"

	#echo -e "\nprev = $prev, cur = $cur, firstword = $firstword"

	case "${firstword}" in
		product)
			case "${prev}" in
				--field)
					suggestions="$PRODUCT_OPTION_FIELD_COMPLETE"
					;;
				*)
					suggestions="$PRODUCT_COMPLETE"
					;;
			esac
			;;
		package)
			suggestions="$PACKAGE_COMPLETE"
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

