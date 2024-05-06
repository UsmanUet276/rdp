def generate_chunks(start, end):
    chunks = []
    current = start
    while current <= end:
        chunk_end = min(current + 999, end)
        chunks.append((current, chunk_end))
        current = chunk_end + 1
    return chunks

start_number = 500001
end_number = 515500
chunks = generate_chunks(start_number, end_number)

for chunk in chunks:
    print(f"{chunk[0]} to {chunk[1]}")