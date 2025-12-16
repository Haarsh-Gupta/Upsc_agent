
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re


class SafeMarkdownSplitter(RecursiveCharacterTextSplitter):
    """
    Prevents splitting inside <table>...</table> and <img ...>.
    Repairs broken chunks by merging small, incomplete, or context-dependent pieces
    forward into the next chunk.
    """

    TABLE_PATTERN = r"(<table.*?</table>)"
    IMG_PATTERN = r"(<img[^>]*>)"

    def split_text(self, text):
        # -------- STEP 1: Protect entire <table>...</table> blocks --------
        blocks = re.split(self.TABLE_PATTERN, text, flags=re.DOTALL)
        raw_chunks = []

        for block in blocks:
            if block.strip().startswith("<table"):
                raw_chunks.append(block)  # keep table whole
                continue

            # -------- STEP 2: Protect <img ...> groups --------
            pieces = re.split(self.IMG_PATTERN, block)

            for p in pieces:
                if p.strip().startswith("<img"):
                    raw_chunks.append(p)  # full <img> tag stays atomic
                else:
                    # Apply normal splitting to text-only
                    if p.strip():
                        raw_chunks.extend(super().split_text(p))

        # -------- STEP 3: Merge fragments to ensure high-quality chunks --------
        final_chunks = self.merge_forward(raw_chunks)
        return final_chunks

    # ---------------------------------------------------------------------
    # LOGIC TO MERGE SMALL / BROKEN / INCOMPLETE CHUNKS FORWARD
    # ---------------------------------------------------------------------
    def merge_forward(self, chunks):
        merged = []
        i = 0

        while i < len(chunks):
            ch = chunks[i].rstrip()

            # ---------- RULE 1: Very small chunks ----------
            is_small = len(ch) < 60 or ch.count("\n") <= 0

            # ---------- RULE 2: Broken <img> tag ----------
            broken_img = ("<img" in ch and ">" not in ch)

            # ---------- RULE 3: Next chunk is a table ----------
            next_is_table = (
                i + 1 < len(chunks) and "<table" in chunks[i + 1]
            )

            # If this chunk requires merging forward
            if is_small or broken_img or next_is_table:
                if i + 1 < len(chunks):
                    # merge with next chunk
                    merged_chunk = ch + "\n" + chunks[i + 1]
                    merged.append(merged_chunk)
                    i += 2
                    continue

            # Otherwise keep as-is
            merged.append(chunks[i])
            i += 1

        return merged


splitter = SafeMarkdownSplitter(
    chunk_size=1200,
    chunk_overlap=150,
    separators=[
        r"(?=\n#{1,6} )",   
        r"\n\n+",
        r"\n",
        " ",
        ""
    ],
    keep_separator=True
)
