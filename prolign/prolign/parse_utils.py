# ----------------------------------------------------------------------------------------------------------------------
# Parsing Functions
# ----------------------------------------------------------------------------------------------------------------------

def fasta_sequence_parser(fasta_sequence: str, fetched=False) -> (str, str):
    """
    Parses a FASTA sequence and extracts the header and sequence.

    :param fasta_sequence: str, the FASTA sequence to be parsed.
    :param fetched: bool, optional (default=False). Specifies whether the FASTA sequence has been fetched from a database
                    or obtained directly as a string. If True, the line separator used is '\n'; if False, it is '\r\n'.
    :return: tuple (str, str), Returns a tuple containing the extracted header and the sequence.
    """
    if not fetched:
        fasta_sequence = fasta_sequence.strip().split("\r\n")
    else:
        fasta_sequence = fasta_sequence.strip().split("\n")

    fasta_header = fasta_sequence[0].split(" ")[0].lstrip(">")
    sequence = "".join(fasta_sequence[1:]).upper()

    return fasta_header, sequence


def text_sequence_parser(text_sequence: str) -> str:
    """
    Parses a text sequence and returns the parsed sequence as a string.

    :param text_sequence: str, the text sequence to be parsed.
    :return: str, Returns the parsed sequence in uppercase, with leading and trailing newline and carriage return characters removed.
    """
    sequence = text_sequence.strip("\n").strip("\r").upper()
    return sequence

