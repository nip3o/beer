set PROJECT_ROOT (dirname $argv[1])
set VIRTUAL_ENV_DIR $PROJECT_ROOT/.venv

if not test -e $VIRTUAL_ENV_DIR
	virtualenv $VIRTUAL_ENV_DIR
end

if set -q $VIRTUAL_ENV
	. $VIRTUAL_ENV_DIR/bin/activate.fish
end

if set -q $DJANGO_SETTINGS_MODULE
	set -gx DJANGO_SETTINGS_MODULE "mb.conf.settings.development"
	set -gx PYTHONPATH "."
end

set -gx VIRTUAL_ENV beer

if test -f .env.local.fish
    . .env.local.fish
end
