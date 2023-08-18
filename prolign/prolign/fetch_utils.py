import requests


# ----------------------------------------------------------------------------------------------------------------------
# Sequence Fetching Functions
# ----------------------------------------------------------------------------------------------------------------------

def ncbi_sequence_fetcher(ncbi_accession_id: str) -> str:
    """
    Fetches the protein sequence in FASTA format for a given NCBI Accession ID.

    :param ncbi_accession_id: str, the NCBI Accession ID of the desired protein.
    :return: str, Returns the protein sequence in FASTA format.
    """

    url = f"https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id={ncbi_accession_id}&db=protein&report=fasta&extrafeat=null&conwithfeat=on&hide-cdd=on&retmode=html&withmarkup=on&tool=portal&log$=seqview&maxdownloadsize=1000000"
    fasta_sequence = requests.get(url).text
    return fasta_sequence


def pdb_sequence_fetcher(pdb_accession_id: str) -> str:
    """
    Fetches the protein sequence in FASTA format for a given PDB Accession ID.

    :param pdb_accession_id: str, the PDB Accession ID of the desired protein.
    :return: str, Returns the protein sequence in FASTA format.
    """
    url = f"https://rest.uniprot.org/uniprotkb/{pdb_accession_id}.fasta"
    fasta_sequence = requests.get(url).text
    return fasta_sequence
