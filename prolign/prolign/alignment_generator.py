import numpy as np
from numpy import ndarray


# ----------------------------------------------------------------------------------------------------------------------
# Global Alignment Generator Function
# ----------------------------------------------------------------------------------------------------------------------


def needleman_wunsch_global_alignment(seq1: str, seq2: str, match_score: int, mismatch_score: int,
                                      gap_penalty: int) -> tuple:
    """
    Performs global alignment of protein sequences using the Needleman-Wunsch algorithm.

    :param seq1: str, the first protein sequence.
    :param seq2: str, the second protein sequence.
    :param match_score: int, the score assigned to a match between two amino acids.
    :param mismatch_score: int, the score assigned to a mismatch between two amino acids.
    :param gap_penalty: int, the penalty for introducing a gap in the alignment.
    :return: tuple, containing the aligned sequences and the alignment score.

    Note:
    - The algorithm constructs a dynamic programming matrix to find the optimal alignment.
    - The match/mismatch scores and gap penalty are used to compute the scores in the matrix.
    - Backtracking through the matrix yields the aligned sequences.
    """

    # Initialize the dynamic programming matrix
    dp_matrix = np.zeros((len(seq1) + 1, len(seq2) + 1), dtype=int)

    # Fill the first row and column with gap penalties
    for i in range(1, len(seq1) + 1):
        dp_matrix[i][0] = dp_matrix[i - 1][0] + gap_penalty
    for j in range(1, len(seq2) + 1):
        dp_matrix[0][j] = dp_matrix[0][j - 1] + gap_penalty

    # Fill the rest of the matrix and compute scores
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            match = dp_matrix[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_score)
            delete = dp_matrix[i - 1][j] + gap_penalty
            insert = dp_matrix[i][j - 1] + gap_penalty
            dp_matrix[i][j] = max(match, delete, insert)

    # Backtrack to find the aligned sequences
    aligned_seq1 = ""
    aligned_seq2 = ""
    i, j = len(seq1), len(seq2)
    while i > 0 or j > 0:
        if i > 0 and dp_matrix[i][j] == dp_matrix[i - 1][j] + gap_penalty:
            aligned_seq1 = seq1[i - 1] + aligned_seq1
            aligned_seq2 = "-" + aligned_seq2
            i -= 1
        elif j > 0 and dp_matrix[i][j] == dp_matrix[i][j - 1] + gap_penalty:
            aligned_seq1 = "-" + aligned_seq1
            aligned_seq2 = seq2[j - 1] + aligned_seq2
            j -= 1
        else:
            aligned_seq1 = seq1[i - 1] + aligned_seq1
            aligned_seq2 = seq2[j - 1] + aligned_seq2
            i -= 1
            j -= 1

    return aligned_seq1, aligned_seq2
