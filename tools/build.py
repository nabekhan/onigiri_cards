from pathlib import Path
import genanki

IDS = {
    "basic": {
        "model_id": 2079419816,
        "deck_id": 2014108329,
        "note_id": 1132448924
    },
    "basic_reverse": {
        "model_id": 2093908175,
        "deck_id": 1435484791,
        "note_id": 1288307408
    },
    "cloze": {
        "model_id": 1828110926,
        "deck_id": 1534501371,
        "note_id": 2068778828
    }
}

# Sample content for the demo cards
NOTE_FIELDS = {
    "basic": ["What is Onigiri?", "A native-styled, flat Anki theme made for the Onigiri addon."],
    "basic_reverse": ["Front Content", "Back Content"],
    "cloze": ["Onigiri is a {{c1::native-styled}} Anki theme for Onigiri.", "Extra info here."]
}

# Setup Paths
root = Path(__file__).parent.parent.resolve()
src_path = root / "src"
template_path = src_path / "templates"
output_path = root / "dist"
output_path.mkdir(exist_ok=True)


def build_package():
    css_file_path = src_path / "css" / "_onigirinote.css"
    js_file_path = src_path / "js" / "_onigirinote.js"

    all_decks = []

    for nt_name, ids_data in IDS.items():
        # Load Template HTML
        front_file = template_path / nt_name / f"{nt_name}-front.html"
        back_file = template_path / nt_name / f"{nt_name}-back.html"

        if not front_file.exists() or not back_file.exists():
            print(f"Skipping {nt_name}: Template files not found.")
            continue

        with open(front_file, "r") as f:
            front_html = f.read()
        with open(back_file, "r") as f:
            back_html = f.read()

        # Handle Template Logic
        if nt_name == "basic_reverse":
            templates = [
                {"name": "Forward", "qfmt": front_html, "afmt": back_html},
                {
                    "name": "Reverse",
                    "qfmt": front_html.replace("Front", "Back"),
                    "afmt": back_html.replace("Back", "Front").replace("Front", "Back", 1)
                }
            ]
        else:
            templates = [{"name": "Card 1", "qfmt": front_html, "afmt": back_html}]

        # Define Model with @import
        model = genanki.Model(
            model_id=ids_data["model_id"],
            name=f"Onigiri {nt_name.replace('_', ' ').title()}",
            fields=[
                {"name": "Text" if nt_name == "cloze" else "Front"},
                {"name": "Back Extra" if nt_name == "cloze" else "Back"},
            ],
            templates=templates,
            css='@import url("_onigirinote.css");',
            model_type=genanki.Model.CLOZE if nt_name == "cloze" else genanki.Model.FRONT_BACK
        )

        # Define Deck
        deck = genanki.Deck(
            ids_data["deck_id"],
            f"Onigiri Notes::{nt_name.replace('_', ' ').capitalize()}"
        )

        # Create Note
        note = genanki.Note(
            guid=ids_data["note_id"],
            model=model,
            fields=NOTE_FIELDS.get(nt_name),
            tags=["onigiri"]
        )

        deck.add_note(note)
        all_decks.append(deck)

    # Bundle Package
    package = genanki.Package(all_decks)
    package.media_files = [str(css_file_path), str(js_file_path)]

    package_file = output_path / "onigiri.apkg"
    package.write_to_file(package_file)

    print(f"Build successful: {package_file}")


if __name__ == "__main__":
    build_package()