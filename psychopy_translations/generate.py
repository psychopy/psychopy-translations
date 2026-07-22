import argparse
from pathlib import Path

# setup call args
argparser = argparse.ArgumentParser(
    prog="psychopy_translations.generate",
    description="Generate .json or .mo files in a given folder from the .po files in this module."
)
argparser.add_argument(
    "folder",
    help="Folder to generate .json/.mo files in",
    type=Path
)
argparser.add_argument(
    "format",
    help="Type of file to generate (json or mo)",
    default="mo",
    choices=[
        "json",
        "mo"
    ]
)
args = argparser.parse_args()


# for each language...
for file in (Path(__file__).parent / "locale").glob("**/*.po"):
    # get language code
    code = file.parent.parent.stem.replace("_", "-")
    # if requested json...
    if args.format == "json":
        import pojson
        import json
        # convert to JSON
        raw = pojson.convert(file)
        data = json.loads(raw)
        # reduce to one entry per phrase
        processed = {
            key: val[1]
            for key, val in data.items()
            if isinstance(val, list) and len(val) == 2
        }
        # save
        (args.folder / f"{code}.json").write_text(
            json.dumps(processed, indent=4), 
            encoding="utf-8"
        )
    # if requested mo...
    if args.format == "mo":
        import polib
        # load po file
        po = polib.pofile(file)
        # save as mo file
        po.save_as_mofile(
            args.folder / f"{code}.mo"
        )