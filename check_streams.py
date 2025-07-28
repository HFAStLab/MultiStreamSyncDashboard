from pylsl import resolve_streams

print("\n[INFO] Active LSL streams:\n")

for s in resolve_streams():

    print(f"Name: {s.name()}, Type: {s.type()}, Source ID: {s.source_id()}")

 