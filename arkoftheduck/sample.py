"""A representative sample document used by the demo/CLI and tests."""

from .model import (
    Checklist, ChecklistItem, Divider, Document, Heading, KeyValues, Paragraph, Table,
)


def build_sample() -> Document:
    doc = Document(
        title="Emergency Preparedness Snapshot",
        meta={"source": "ark.sample", "profile": "default"},
    )
    doc.add(Paragraph(
        "The same data below renders identically well as plain text on a 1990s "
        "terminal, as a colorful CLI, as Markdown, JSON, CSV, or a web page. It "
        "always works."
    ))
    doc.add(Heading("Top Risks", level=1))
    doc.add(Table(
        caption="Probability x Impact (sample)",
        headers=["Hazard", "Probability", "Impact", "Priority"],
        rows=[
            ["Earthquake", "Medium", "High", "1"],
            ["Extended power outage", "High", "Medium", "2"],
            ["Wildfire", "Low", "High", "3"],
            ["Flood", "Low", "Medium", "4"],
        ],
    ))
    doc.add(Heading("72-Hour Kit", level=1))
    doc.add(Checklist(items=[
        ChecklistItem("Water: 3 gallons per person", done=True, priority="high"),
        ChecklistItem("Non-perishable food: 3 days", done=True, priority="high"),
        ChecklistItem("First aid kit + medications", done=False, priority="high"),
        ChecklistItem("Flashlight + spare batteries", done=False, priority="medium"),
        ChecklistItem("Battery/hand-crank radio", done=False, priority="medium"),
        ChecklistItem("Copies of documents", done=False, priority="low"),
    ]))
    doc.add(Divider())
    doc.add(KeyValues(title="Household", pairs=[
        ("Adults", "2"),
        ("Children", "1"),
        ("Pets", "1 dog"),
        ("Readiness score", "62%"),
    ]))
    return doc
