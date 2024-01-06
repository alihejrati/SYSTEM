# Note: git version 2.34.1 has been used in development.


# Note:
# (color) Red   -> working directory != stage directory  (from that file, point of view)
# (color) Green -> working directory == stage directory  (from that file, point of view)
# (command) commit -> save a snapshot of stage directory into repository
# (notic) after doing commit, stage directory is still alive.
# (notic) head: specefic commit in repository. [default value: latest commit]
# (define) commit it means saving a snapshot of `stage directory` to repository.
# (define) each commit in repository is a snapshot of stage directory.
# (define) each commit is specefic snapshot of stage.
# (sync) -> file or pattern that discribe files, between two point.
# (diff) -> all files between two point.

kg-version ()
{
	eval "git --version"
}

kg-configuration () # set config params.
{
    set -- "${1:-$K_GIT_NAME}" "${2:-$K_GIT_EMAIL}" "${3:-local}" "${4:-main}" "${5:-nano}"
	eval "git config --$3 user.name \"$1\""
	eval "git config --$3 user.email \"$2\""
	eval "git config --$3 core.editor \"$5\"" #vscode -> code --wait
	eval "git config --$3 core.autocrlf input" # mac/linux -> input | windows -> true
	eval "git config --$3 init.defaultBranch \"$4\""
	eval "git config --$3 -e" # open configuration file in default editor
    # system -> all users
    # global -> all repositories of the current user
    # local  -> the current repository
}

kg-configuration-print () # show config file.
{
	set -- "${1:-local}" # system, global, local
	eval "git config --$1 -e"
}

kg-init () # initilize a repository.
{
    set -- "${1:-~/my-project}"
	eval "k-cd \"$1\""
	eval "rm -rf .git"
	eval "git init"
	eval "echo \".gitignore\" > .gitignore"
	eval "kg-configuration"
}

kg-status () # status between workdir vs stage
{
	eval "git status -s" # output -> (stage_dir, working_dir, filename)
	eval "k-underline"
}

# Note: we have command `ls` for workdir.
kg-ls-stage () # ls inside stage directory
{
	eval "git ls-files"
	eval "k-underline"
}

kg-ls-repo () # ls inside repo at specefic commit determined by identifire
{
	set -- "${1:-HEAD~0}" # identifire or HEAD~n
	eval "git ls-tree $1" # Note: in outout if this command: blob -> file and tree -> directory
	eval "k-underline"
}

# Note: we have command `rm -rf` for workdir.
kg-rm-stage () # only remove file from stage directory
{
	eval "git rm --cached -rf \"$1\""
}

kg-rm-both () # remove file from `workdir` and `stage`
{
	eval "git rm -rf \"$1\""
}

# Note: we have command `cat` for workdir.
kg-cat-stage () # cat file on stage. # $1 is `file path` on stage.
{
	eval "git show :$1"
	eval "k-underline"
}

kg-cat-repo ()
{
	# $1: identifire or HEAD~n  # Note: if identifire is belong to file then will show content of it. (file identifire can be found trough `kg-ls-repo HEAD~n`)
	# $2: file path
	set -- "${1:-HEAD~0}" "${2:-}" 
	eval "git show $1:$2"
	eval "k-underline"
}

kg-cat-repo-fid () # cat file on specefic commit of repo. # $1 is `file identifire` on repo commited snapshot.
{
	eval "git show $1"
	eval "k-underline"
}

# Note: high level view of repository at specefic branch.
kg-repository () # detailing view
{
	if [ -z "$1" ]
	then
		eval "git log"
	else
		eval "git show $1"
	fi
	eval "k-underline"
}

kg-repo () # short view
{
	if [ -z "$1" ]
	then
		eval "git log --oneline"
	else
		eval "git show $1"
	fi
	eval "k-underline"
}

# Note: 1) diff operation conssiders all files. 2) diff is a forward operation from (work_dir to [stage or head]) or from (stage to head)
kg-diff-workdir-stage () # The `git diff` command displays the changes between the working directory and the staging area.
{
	eval "git diff"
	eval "k-underline"
}

kg-diff-workdir-repo () # workdir vs specefic commit of repository.
{
	set -- "${1:-HEAD~0}"
	eval "git diff $1" 
	eval "k-underline"
}

kg-diff-stage-repo () # stage vs specefic commit of repository.
{
	set -- "${1:-HEAD~0}"
	eval "git diff $1 --staged" #eval "git diff --cached"  --> (--staged is a synonym for --cached)
	eval "k-underline"
}

# Note: syncronizing files.
kg-sync-repo2workdir () # overwrite file from repo to workdir. if file doesnt exist in repo then file gonna be delete from workdir.
{
	set -- "${1:-HEAD~0}" "${2:-.}"
	# $1: identifire -> hashID or HEAD~n
	# $2: file path we want overwrite it from repo(specefic commit) to workdir.
	eval "git restore --source=$1 $2"
}

kg-sync-repo2stage () # overwrite file from repo to stage. if file doesnt exist in repo then file gonna be delete from stage.
{
	set -- "${1:-HEAD~0}" "${2:-.}"
	# $1: identifire -> hashID or HEAD~n
	# $2: file path we want overwrite it from repo(specefic commit) to stage.
	eval "git restore --staged --source=$1 $2"
}

kg-sync-stage2repo () # commit operation. # overwriting a commit does not make sence anyway, so we take a new snapshot and we create it in a new commit on repository.
{
	set -- "${1:-Taking snapshot of stage directory.}"
	# $1: msg -> hashID or HEAD~n
	eval "git commit -m $1"
}

kg-sync-workdir2stage () # add operation. # overwrite file from workdir to stage. if file doesnt exist in workdir then file gonna be delete from stage.
{
	set -- "${1:-.}" # default is all files.
	# $1: file path
	eval "git add $1"
}

kg-sync-stage2workdir () # overwrite file from stage to workdir. # Note: if file doesnt exist in stage then file `doesnt` gonna be delete from workdir (git policy: stage->workdir).
{ # Discarding local changes.
	set -- "${1:-.}"
	# $1: file path we want overwrite it from stage to workdir.
	eval "git restore $1"
}

kg-sync-stage2workdir-clean () # overwrite file from stage to workdir. if file doesnt exist in stage then file gonna be delete from workdir.
{ # Discarding local changes.
	set -- "${1:-.}"
	# $1: file path we want overwrite it from stage to workdir.
	eval "git restore $1"
	eval "git clean -fd" # Note: if there is a file or directory in workdir such that those are not been in stage, git will gonna delete those files or directories.
}

# Note: Search for commits (by author, date, message, etc...) Find a bad commit that introduced a bug.











# NOTE: examples of git commands.
kg-ex-f0 ()
{
	kg-status
	kg-ls-stage
	ls
	k-underline
}
kg-ex1 ()
{
	kg-init $(k-strrand)
	kg-ex-f0
	echo "hello" > file1.txt # unstaged file
	echo "hello" > file2.txt # unstaged file
	kg-ex-f0
	git add . # transfering file to stage
	git commit -m fs # taking snapshot from `stage` and saveing it on `repository` as `commit` in `branch`.
	kg-ex-f0
	kg-repo
	kg-ls-repo
	echo "hello world" >> file1.txt
	touch file3.txt
	kg-ex-f0
	git add .
	git commit -m sc
	kg-ex-f0
	kg-repo
	kg-ls-repo # this line take `ls` inside HEAD~0
	kg-repo HEAD~1 # identifire -> hashID or HEAD~n # Note: this line show diff information of commit.
	kg-ls-repo HEAD~1 # identifire -> hashID or HEAD~n
	k-underline +
	# kg-cat-repo-fid ce013625030ba8dba906f756967f9e9ca394464a # Note: fid is unique for each file since I comment it here.
	kg-cat-repo HEAD~0 file1.txt
	kg-cat-repo HEAD~1 file1.txt
	kg-cat-stage file1.txt
	cat file1.txt
	k-underline +
	echo "---> stage>file1.txt has been overwrite from HEAD~1:file1.txt of repository."
	kg-sync-repo2stage HEAD~1 file1.txt
	kg-ex-f0
	kg-cat-repo HEAD~0 file1.txt
	kg-cat-repo HEAD~1 file1.txt
	kg-cat-stage file1.txt
	cat file1.txt
	k-underline =
	echo "---> workdir>file1.txt changed now."
	echo "new change" >> file1.txt
	k-underline +
	kg-ex-f0
	kg-cat-repo HEAD~0 file1.txt
	kg-cat-repo HEAD~1 file1.txt
	kg-cat-stage file1.txt
	cat file1.txt
	k-underline ^
	echo "---> diff stage vs HEAD~0 from repository."
	kg-diff-stage-repo
	k-underline ^
	echo "---> diff stage vs HEAD~1 from repository."
	kg-diff-stage-repo HEAD~1
	k-underline ^
	echo "---> diff workdir vs stage"
	kg-diff-workdir-stage
	k-underline ^
	echo "---> diff workdir vs repo HEAD~0"
	kg-diff-workdir-repo HEAD~0
	k-underline ^
	echo "---> diff workdir vs repo HEAD~1"
	kg-diff-workdir-repo HEAD~1
}