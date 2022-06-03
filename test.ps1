param(
    [Parameter(Mandatory = $false)][switch]$ROOT_DIR="test",
    [Parameter(Mandatory = $false)][switch]$DIRECTORIES=@("log", "data", "archive", "temp")
)


if (!(Test-Path -Path $ROOT_DIR ))
{
    New-Item -ItemType Directory -Path $ROOT_DIR
}

foreach ($DIR in $DIRECTORIES)
{
    if (!(Test-Path -Path $DIR ))
    {
        New-Item -ItemType "Directory" -Path "$ROOT_DIR/$DIR"
    }
}

python main.py
