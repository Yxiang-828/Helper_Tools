import os
import UnityPy
import argparse

"""Convert Unity3D document bundles into a single markdown file.

This tool loads the specified .unity3d file (or all .unity3d files in
a directory) and writes every TextAsset it contains to a markdown file.
Each asset is separated by a heading so the resulting document is easy to
scan in a text editor or viewer.

Usage examples:
    python 32_unity_to_md.py "C:\path\to\AllLanguageEN.unity3d"
    python 32_unity_to_md.py "C:\path\to\directory" -o output.md
"""


def convert_bundle(input_path: str, output_file: str):
    """Load a unity3d bundle and append its text assets to output_file."""
    try:
        env = UnityPy.load(input_path)
    except Exception as exc:
        print(f"Failed to load {input_path}: {exc}")
        return 0

    count = 0
    with open(output_file, "a", encoding="utf-8") as f:
        for obj in env.objects:
            if obj.type.name == "TextAsset":
                data = obj.read()
                # try decoding, skip if not utf-8
                try:
                    text = data.script.decode("utf-8")
                except Exception:
                    continue
                f.write(f"## {data.name}\n\n")
                f.write(text)
                f.write("\n\n")
                count += 1
    return count


def main():
    parser = argparse.ArgumentParser(
        description="Convert Unity3D document bundles to markdown."
    )
    parser.add_argument("source", help="Unity3D file or directory to process")
    parser.add_argument(
        "-o",
        "--output",
        help="Path of the markdown file to create. If omitted the output will be created next to the first bundle with a .md extension.",
    )

    args = parser.parse_args()
    source = args.source

    if os.path.isdir(source):
        # find all unity3d files
        files = []
        for root, _, filenames in os.walk(source):
            for fn in filenames:
                if fn.lower().endswith(".unity3d"):
                    files.append(os.path.join(root, fn))
    else:
        files = [source]

    if not files:
        print(f"No unity3d files found in {source}")
        return

    # determine output file
    out = args.output
    if not out:
        base = os.path.splitext(os.path.basename(files[0]))[0]
        out = os.path.join(os.getcwd(), base + ".md")

    # make sure output file is empty
    open(out, "w", encoding="utf-8").close()

    total = 0
    for fpath in files:
        print(f"Processing {fpath}")
        count = convert_bundle(fpath, out)
        print(f"  extracted {count} text assets")
        total += count

    print(f"Wrote {total} assets into {out}")


if __name__ == "__main__":
    main()
