k-argparse () # specify an arbitrary list of arguments:
{
    output=$(eval "$K_COMPILER_PY $K_ROOT_DIR/python/argparse_handler.py $@")
    eval "$output"
}


k-cd ()
{
    eval "mkdir -p $1 && cd $1"
}

k-strrand ()
{
    set -- "${1:-13}"
    eval "echo $(openssl rand -hex $1)"
}

k-reload ()
{
    eval "source ~/Documents/Code/bashscript/alias.bash"
}

k-underline ()
{
    set -- "${1:--}"
    eval "printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' $1"
}

k-ls ()
{
    eval "ls"
    eval "k-underline"
}

k-ll ()
{
    eval "ll"
    eval "k-underline"
}

k-ls-disk ()
{
    eval "lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL -e7"
    eval "k-underline"
}

k-dmg2iso ()
{
    set -- "${1:--}"
    echo "help) install: sudo apt-get install dmg2img"
    eval "sudo dmg2img -v -i \"$1.dmg\" -o \"$1.iso\""
}

k-iso2boot ()
{
    set -- "${1:--}" "${2:--sdb}"
    echo "help) for macos, you need convert dmg to iso: k-dmg2iso filepath_without_extention"
    eval "sudo dd if=\"$1.iso\" of=\"/dev/$2\" && sync"
}

k-zip ()
{
    set -- "${1:--}"
    eval "zip -r \"$(realpath -s $1).zip\" $1"
}

k-unrar ()
{
    eval "unrar x -p './*.rar'"
}

